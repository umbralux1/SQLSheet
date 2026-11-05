"""Quick checks before running or deploying. Needs only the standard library.

* main.py and course.py are valid Python;
* every task has a unique id (progress is saved by task id), its texts and explanations;
* course_results.json is up to date: `make results` ran every query of the current course
  on PostgreSQL (PGlite) and stopped on any that failed;
* the course sent to browsers (/course.js) contains no answers or teacher tips.

Usage: python scripts/check.py   (or: make check)
"""
import ast
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
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

from build_results import OUTPUT, lesson_hash  # noqa: E402
from course import COURSE  # noqa: E402

results = json.loads(OUTPUT.read_text(encoding="utf-8")) if OUTPUT.exists() else None
if results is None:
    fail(f"{OUTPUT.name} is missing: run `make results`")
else:
    print(f"  ✓ results from {results['engine'].split(' on ')[0]}")

for lesson in COURSE["lessons"]:
    if not lesson.get("available"):
        continue
    lid, tasks = lesson["id"], lesson["tasks"]
    bad = 0
    ids = [t.get("id") for t in tasks]
    if None in ids or len(set(ids)) != len(ids):
        bad += 1
        fail(f"lesson {lid}: every task needs its own unique \"id\" (progress is saved by it)")
    for i, task in enumerate(tasks, 1):
        kind = task.get("kind")
        needed = {"row": "condition", "pick": "condition", "rewrite": "answer", "value": "expr", "truth": "cols"}.get(kind, "answer")
        if needed not in task:
            bad += 1
            fail(f"lesson {lid}, task {i}: no {needed}")
        if (kind in ("row", "pick", "rewrite", "value")) and not all(k in task.get("explain", {}) for k in ("en", "ru")):
            bad += 1
            fail(f"lesson {lid}, task {i}: this kind of task needs an en and ru explanation")
        for key in ("en", "ru"):
            if key not in task["text"]:
                bad += 1
                fail(f"lesson {lid}, task {i}: missing {key} text")
    if results is not None and results["lessons"].get(str(lid), {}).get("hash") != lesson_hash(lesson):
        bad += 1
        fail(f"lesson {lid}: changed since the results were worked out: run `make results`")
    if not bad:
        print(f"  ✓ lesson {lid}: {len(tasks)} tasks")

# The public course must not leak answers or tips (same code as /course.js).
if results is not None:
    source = (ROOT / "main.py").read_text(encoding="utf-8")
    start, end = source.index("def public_course"), source.index("def find_lesson")
    namespace = {"COURSE": COURSE, "RESULTS": results}
    exec(source[start:end], namespace)
    public = json.dumps(namespace["public_course"]())
    if re.search(r'"(answer|tips|explain)"', public):
        fail("/course.js would contain answers, explanations or tips")
    else:
        print("  ✓ /course.js has no answers, explanations or tips")

if errors:
    print(f"\n{len(errors)} problem(s) found.")
    sys.exit(1)
print("\nAll checks passed.")
