"""Quick checks before running or deploying. Needs only the standard library.

* main.py and course.py are valid Python;
* every lesson's seed loads, and every task answer and section example runs;
* every task has a unique id (progress is saved by task id);
* the course sent to browsers (/course.js) contains no answers or teacher tips.

Usage: python scripts/check.py   (or: make check)
"""
import ast
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
errors = []


def fail(message: str) -> None:
    errors.append(message)
    print(f"  ✗ {message}")


for name in ("main.py", "course.py"):
    try:
        ast.parse((ROOT / name).read_text(encoding="utf-8"))
        print(f"  ✓ {name} parses")
    except SyntaxError as e:
        fail(f"{name}: {e}")

from course import COURSE  # noqa: E402

for lesson in COURSE["lessons"]:
    if not lesson.get("available"):
        continue
    lid, tasks = lesson["id"], lesson["tasks"]
    con = sqlite3.connect(":memory:")
    try:
        con.executescript(lesson["seed"])
    except sqlite3.Error as e:
        fail(f"lesson {lid}: seed does not load: {e}")
        continue
    bad = 0
    ids = [t.get("id") for t in tasks]
    if None in ids or len(set(ids)) != len(ids):
        bad += 1
        fail(f"lesson {lid}: every task needs its own unique \"id\" (progress is saved by it)")
    table = (lesson.get("tables") or [None])[0]
    for i, task in enumerate(tasks, 1):
        if task.get("kind") in ("row", "pick"):           # prediction tasks: a condition instead of an answer
            tname = task.get("table", table)
            try:
                rows = con.execute('SELECT * FROM "%s" WHERE %s' % (tname, task["condition"])).fetchall()
                if task["kind"] == "row":
                    key = con.execute('PRAGMA table_info("%s")' % tname).fetchone()[1]   # first column, e.g. emp_id
                    if not con.execute('SELECT 1 FROM "%s" WHERE %s = ?' % (tname, key), (task["row"],)).fetchone():
                        bad += 1
                        fail(f"lesson {lid}, task {i}: row {task['row']} does not exist")
            except (sqlite3.Error, KeyError) as e:
                bad += 1
                fail(f"lesson {lid}, task {i}: condition fails: {e}")
            if not all(k in task.get("explain", {}) for k in ("en", "ru")):
                bad += 1
                fail(f"lesson {lid}, task {i}: prediction task needs an en and ru explanation")
        elif task.get("kind") in ("value", "truth"):     # logic tasks: an expression instead of an answer
            exprs = [task.get("expr")] if task["kind"] == "value" else task.get("cols", [])
            names = list(task.get("given", {})) if task["kind"] == "value" else task.get("vars", [])
            try:
                if not all(exprs):
                    raise KeyError("expr / cols")
                frm = (" FROM (SELECT " + ", ".join("1 AS %s" % n for n in names) + ")") if names else ""
                for e in exprs:
                    con.execute("SELECT (%s)%s" % (e, frm)).fetchall()
            except (sqlite3.Error, KeyError) as e:
                bad += 1
                fail(f"lesson {lid}, task {i}: expression fails: {e}")
            if task["kind"] == "value" and not all(k in task.get("explain", {}) for k in ("en", "ru")):
                bad += 1
                fail(f"lesson {lid}, task {i}: \"value\" task needs an en and ru explanation")
        elif "answer" not in task:
            bad += 1
            fail(f"lesson {lid}, task {i}: no answer")
        for field in ("answer", "example"):
            if field in task:
                try:
                    con.execute(task[field]).fetchall()
                except sqlite3.Error as e:
                    bad += 1
                    fail(f"lesson {lid}, task {i}: {field} fails: {e}")
        for key in ("en", "ru"):
            if key not in task["text"]:
                bad += 1
                fail(f"lesson {lid}, task {i}: missing {key} text")
    if not bad:
        print(f"  ✓ lesson {lid}: {len(tasks)} tasks, answers and examples run")

# The public course must not leak answers or tips (same code as /course.js).
source = (ROOT / "main.py").read_text(encoding="utf-8")
start, end = source.index("def public_course"), source.index("def find_lesson")
namespace = {"COURSE": COURSE}
exec(source[start:end], namespace)
public = json.dumps(namespace["public_course"]())
if '"answer"' in public or '"tips"' in public or '"explain"' in public:
    fail("/course.js would contain answers, explanations or tips")
else:
    print("  ✓ /course.js has no answers, explanations or tips")

if errors:
    print(f"\n{len(errors)} problem(s) found.")
    sys.exit(1)
print("\nAll checks passed.")
