"""Works out the course's expected results on PostgreSQL (PGlite) and saves them to course_results.json.

The server has no database: it checks students' results against this file. Run this after every
change to a lesson's data, answers, examples or conditions, and commit the file. `make check`
fails when the file is out of date. A failing query here means a lesson is broken.

Needs Node: run `npm install` once.   Usage: python scripts/build_results.py   (or: make results)
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from course import COURSE  # noqa: E402

OUTPUT = ROOT / "course_results.json"
_CHECKED_FIELDS = ("id", "kind", "answer", "example", "condition", "table", "row", "expr", "cols", "vars",
                   "nulls", "given", "domain", "form")


def lesson_hash(lesson: dict) -> str:
    """Changes whenever something the results depend on changes. Also used by scripts/check.py."""
    tasks = [{k: t[k] for k in _CHECKED_FIELDS if k in t} for t in lesson["tasks"]]
    source = json.dumps([lesson["seed"], lesson.get("tables"), tasks], sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(source.encode()).hexdigest()[:16]


class PgError(Exception):
    pass


class Pg:
    def __init__(self) -> None:
        self.process = subprocess.Popen(["node", str(ROOT / "scripts" / "pg_bridge.mjs")], cwd=ROOT, text=True,
                                        stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def call(self, op: str, **args):
        self.process.stdin.write(json.dumps({"op": op, **args}) + "\n")
        self.process.stdin.flush()
        reply = json.loads(self.process.stdout.readline())
        if "error" in reply:
            raise PgError(reply["error"]["message"])
        return reply["result"]

    def query(self, sql: str) -> dict:
        """The result of the last statement: {columns, rows, ...}."""
        return self.call("run", sql=sql)[-1]

    def close(self) -> None:
        self.process.stdin.close()
        self.process.wait()


def normalize(value):
    """Sums of fractions may differ in the last digits. The same rule as main.py uses for the student's rows."""
    if isinstance(value, float):
        value = round(value, 6)
        if value.is_integer():
            return int(value)
    return value


def sql_val(v) -> str:
    return "TRUE" if v == 1 else "FALSE" if v == 0 else "NULL::boolean"


def sql_lit(v) -> str:
    if isinstance(v, str):
        return "'" + v.replace("'", "''") + "'"
    return "NULL" if v is None else str(v)


def as_bool(expr: str) -> str:
    return f"CASE WHEN ({expr}) THEN 1 WHEN NOT ({expr}) THEN 0 END"


def tv(v) -> str:
    return "true" if v == 1 else "false" if v == 0 else "null"


def truth_rows(t: dict) -> list[list]:
    """Every combination of the variables, TRUE first (then FALSE, then NULL)."""
    rows = [[]]
    for _ in t["vars"]:
        rows = [r + [v] for r in rows for v in ([1, 0, None] if t.get("nulls") else [1, 0])]
    return rows


def rewrite_cases(t: dict) -> tuple[list[str], list[list], object]:
    """The column names, every combination of values, and how to write a value in SQL."""
    if t.get("vars"):
        return t["vars"], truth_rows(t), sql_val
    names, rows = list(t["domain"]), [[]]
    for name in names:
        rows = [r + [v] for r in rows for v in t["domain"][name]]
    return names, rows, sql_lit


def values_cte(names: list[str], rows: list[list], lit) -> str:
    values = ", ".join("(" + ", ".join(lit(v) for v in r) + ")" for r in rows)
    return f"WITH v({', '.join(names)}) AS (VALUES {values})"


# ---------------------------------------------------------------------------
# Sorted answers: rows that are equal in every ORDER BY column may come in any order,
# so a student's rows are compared group by group. The sort keys are read by running the
# answer again with them as extra columns and without LIMIT/OFFSET.
# ---------------------------------------------------------------------------
_ORDER_RE = re.compile(r"\border\s+by\s+(.+?)(?:\s+limit\s+(\d+)(?:\s+offset\s+(\d+))?)?\s*;?\s*$", re.I | re.S)


def split_top(text: str) -> list[str]:
    """Split on commas that are not inside brackets or quotes."""
    parts, depth, quote, cur = [], 0, None, ""
    for ch in text:
        if quote:
            quote = None if ch == quote else quote
        elif ch in "'\"":
            quote = ch
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif ch == "," and depth == 0:
            parts.append(cur)
            cur = ""
            continue
        cur += ch
    return parts + [cur]


def order_groups(pg: Pg, answer: str, columns: list[str]):
    """[start, size, groups, group of each position] for an answer that sorts, or None to compare exactly."""
    answer = answer.strip()
    m = _ORDER_RE.search(answer)
    head = answer[:m.start()] if m else ""
    sel = re.match(r"\s*select\s+(?!distinct\b)", head, re.I)
    frm = re.search(r"\bfrom\b", head, re.I)
    if not (m and sel and frm):
        return None
    n = len(columns)
    parsed = [re.match(r"\s*(.*?)(\s+(?:asc|desc))?(\s+nulls\s+(?:first|last))?\s*$", k, re.I | re.S) for k in split_top(m.group(1))]
    keys = [p.group(1) for p in parsed]
    attempts = []
    if not any(k.isdigit() for k in keys):      # the sort keys as extra columns of the same query
        attempts.append(f"{head[:frm.start()].rstrip()}, {', '.join(keys)} {head[frm.start():]} ORDER BY {m.group(1)}")
    # or the keys are names (ORDER BY revenue) or positions (ORDER BY 2) of the result's columns
    outer = [f'"{columns[int(k) - 1]}"' if k.isdigit() and 0 < int(k) <= n else k for k in keys]
    order = ", ".join(o + (p.group(2) or "") + (p.group(3) or "") for o, p in zip(outer, parsed))
    attempts.append(f"SELECT *, {', '.join(outer)} FROM ({head}) ORDER BY {order}")
    rows = None
    for sql in attempts:
        try:
            rows = pg.query(sql)["rows"]
            break
        except PgError:
            continue
    if rows is None or any(len(r) != n + len(keys) for r in rows):
        return None
    groups, by_pos, last = [], [], object()
    for r in rows:
        key = r[n:]
        if key != last:
            groups.append([])
            last = key
        groups[-1].append(json.dumps([normalize(v) for v in r[:n]]))
        by_pos.append(len(groups) - 1)
    start = int(m.group(3) or 0)
    size = len(rows) - start if m.group(2) is None else max(0, min(int(m.group(2)), len(rows) - start))
    return [start, size, groups, by_pos]


def task_result(pg: Pg, lesson: dict, t: dict) -> dict:
    kind = t.get("kind")
    if kind in ("row", "pick"):
        table = t.get("table", lesson["tables"][0])
        rows = pg.query(f'SELECT * FROM "{table}" WHERE {t["condition"]}')["rows"]
        if kind == "row":
            first_column = pg.query(f'SELECT * FROM "{table}" LIMIT 0')["columns"][0]
            if not pg.query(f'SELECT 1 FROM "{table}" WHERE "{first_column}" = {sql_lit(t["row"])}')["rows"]:
                raise PgError(f"row {t['row']} does not exist")
        return {"passing": [[r[0], r[1]] for r in rows]}
    if kind == "value":
        sql = "SELECT " + as_bool(t["expr"])
        if t.get("given"):
            sql += " FROM (SELECT " + ", ".join(f"{sql_val(v)} AS {k}" for k, v in t["given"].items()) + ")"
        return {"value": tv(pg.query(sql)["rows"][0][0])}
    if kind == "truth":
        sql = values_cte(t["vars"], truth_rows(t), sql_val) + f" SELECT {', '.join(as_bool(c) for c in t['cols'])} FROM v"
        return {"table": [[tv(v) for v in row] for row in pg.query(sql)["rows"]]}
    if kind == "rewrite":
        names, rows, lit = rewrite_cases(t)
        sql = values_cte(names, rows, lit) + f" SELECT {as_bool(t['expr'])}, {as_bool(t['answer'])} FROM v"
        result = pg.query(sql)["rows"]
        if any(a != b for a, b in result):
            raise PgError("the answer does not mean the same as the expression")
        pattern = r"\bnot\b" if t.get("form") == "no_not" else r"\bnot\s*\("
        if re.search(pattern, t["answer"], re.I):
            raise PgError("the answer does not have the asked form")
        return {"original": [r[0] for r in result]}
    result = pg.query(t["answer"])
    columns = result["columns"]
    out = {"columns": columns, "rows": [[normalize(v) for v in row] for row in result["rows"]]}
    if re.search(r"\border\s+by\b", t["answer"], re.I):
        out["order"] = order_groups(pg, t["answer"], columns)
    return out


def main() -> int:
    pg = Pg()
    problems = []
    out = {"engine": pg.call("version"), "previews": {}, "lessons": {}}
    print(out["engine"])
    for lesson in COURSE["lessons"]:
        if not lesson.get("available"):
            continue
        lid = lesson["id"]
        try:
            pg.call("reset", seed=lesson["seed"])
        except PgError as e:
            problems.append(f"lesson {lid}: seed does not load: {e}")
            continue
        out["previews"][lesson.get("seed_ref") or str(lid)] = pg.call("tables")
        tasks, examples, bad = {}, {}, 0
        for i, t in enumerate(lesson["tasks"], 1):
            try:
                tasks[t["id"]] = task_result(pg, lesson, t)
            except PgError as e:
                bad += 1
                problems.append(f"lesson {lid}, task {i} ({t['id']}): {e}\n      {t.get('answer') or t.get('condition') or t.get('expr')}")
            if "example" in t:
                try:
                    r = pg.query(t["example"])
                    examples[t["id"]] = {"columns": r["columns"], "rows": r["rows"]}
                except PgError as e:
                    bad += 1
                    problems.append(f"lesson {lid}, task {i} ({t['id']}): example fails: {e}\n      {t['example']}")
        out["lessons"][str(lid)] = {"hash": lesson_hash(lesson), "tasks": tasks, "examples": examples}
        print(f"  {'✗' if bad else '✓'} lesson {lid}: {len(lesson['tasks'])} tasks")
    pg.close()
    if problems:
        print(f"\n{len(problems)} problem(s), {OUTPUT.name} not written:")
        for p in problems:
            print("  ✗ " + p)
        return 1
    OUTPUT.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"\nWrote {OUTPUT.name} ({OUTPUT.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
