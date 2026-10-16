"""Quick checks before running or deploying. Needs only the standard library.

* main.py and course.py are valid Python;
* every lesson's seed loads, and every task answer and section example runs;
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
    for i, task in enumerate(tasks, 1):
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
if '"answer"' in public or '"tips"' in public:
    fail("/course.js would contain answers or tips")
else:
    print("  ✓ /course.js has no answers or tips")

if errors:
    print(f"\n{len(errors)} problem(s) found.")
    sys.exit(1)
print("\nAll checks passed.")
