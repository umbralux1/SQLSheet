import hashlib
import hmac
import json
import os
import re
import secrets
import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request, Response, WebSocket, WebSocketDisconnect
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field

import psycopg

import pg_engine
from course import COURSE
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="SQL Sheet")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Pages are revalidated on every visit, so a new deploy shows up right away.
NO_CACHE = {"Cache-Control": "no-cache"}


@app.get("/", include_in_schema=False)
async def root():
    """Home page: the SQL trainer with an Excel-style result grid."""
    return FileResponse(STATIC_DIR / "index.html", headers=NO_CACHE)


@app.get("/lessons", include_in_schema=False)
async def lessons():
    """Course page: lesson theory, tables and tasks."""
    return FileResponse(STATIC_DIR / "lessons.html", headers=NO_CACHE)


# ---------------------------------------------------------------------------
# Course data and the teacher account
#
# The browser gets the course from /course.js WITHOUT the answers. Students'
# queries run on the PostgreSQL server (pg_engine.py); their results are checked
# here (/api/check) against course_results.json, which scripts/build_results.py
# works out with the same code. Only the logged-in teacher can read the answers
# (/api/answers/<lesson id>).
#
# Teacher login: user "teacher", password from the TEACHER_PASSWORD environment
# variable (default "sql2026" - change it on Render).
# ---------------------------------------------------------------------------

TEACHER_USER = "teacher"
TEACHER_PASSWORD = os.environ.get("TEACHER_PASSWORD", "sql2026")
SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_hex(32)  # a random key logs everyone out on restart
SESSION_COOKIE = "sqlt_teacher"
RESULTS = json.loads((BASE_DIR / "course_results.json").read_text(encoding="utf-8"))

PROGRESS_JS = """
/* Progress is kept per browser, as a list of solved task ids ("2.10", "2.or3", ...).
   Older versions saved task positions (0, 1, 2, ...). Task ids were numbered from
   those positions, so position n is task "<lesson>.<n+1>" and old progress carries over. */
(window.COURSE.lessons || []).forEach(l => {
  if (l.seed_ref && !l.seed) l.seed = (window.COURSE.seeds || {})[l.seed_ref];
  l.preview = (window.COURSE.previews || {})[l.seed_ref || l.id];
});
window.COURSE_PROGRESS = {
  key: lessonId => 'sqlt-solved-L' + lessonId,
  get(lessonId) {
    let raw = [];
    try { raw = JSON.parse(localStorage.getItem(this.key(lessonId)) || '[]') } catch (e) {}
    return raw.map(v => typeof v === 'number' ? lessonId + '.' + (v + 1) : v);
  },
  add(lessonId, taskId) {
    const s = new Set(this.get(lessonId)); s.add(taskId);
    try { localStorage.setItem(this.key(lessonId), JSON.stringify([...s])) } catch (e) {}
  },
  // solved tasks of a lesson: main tasks by default, extra practice with extra = true
  count(lesson, extra) { const s = new Set(this.get(lesson.id)); return lesson.tasks.filter(t => !!t.extra === !!extra && s.has(t.id)).length }
};
"""


def public_course() -> dict:
    """The course without the answers, the explanations of prediction tasks and the teacher's tips."""
    lessons, counters = [], {}
    for lesson in COURSE["lessons"]:
        track = lesson.get("track", "base")
        counters[track] = counters.get(track, 0) + 1
        item = {k: v for k, v in lesson.items() if k not in ("tasks", "tips")}
        item["track"] = track
        item["num"] = counters[track]          # the number shown to people, inside its course
        if "seed_ref" in lesson:
            item.pop("seed", None)             # shared data is sent once, in "seeds"
        if "tasks" in lesson:
            item["tasks"] = [{k: v for k, v in t.items() if k not in ("answer", "explain")} for t in lesson["tasks"]]
        if lesson.get("available"):
            item["examples"] = RESULTS["lessons"][str(lesson["id"])]["examples"]
        lessons.append(item)
    return {"tracks": COURSE.get("tracks", []), "seeds": COURSE.get("seeds", {}), "previews": RESULTS["previews"], "lessons": lessons}


def find_lesson(lesson_id: int) -> dict:
    for lesson in COURSE["lessons"]:
        if lesson["id"] == lesson_id and lesson.get("available"):
            return lesson
    raise HTTPException(status_code=404, detail="Lesson not found")


def session_token() -> str:
    return hmac.new(SECRET_KEY.encode(), b"teacher", hashlib.sha256).hexdigest()


def is_teacher(request: Request) -> bool:
    return hmac.compare_digest(request.cookies.get(SESSION_COOKIE, "").encode(), session_token().encode())


@app.get("/course.js", include_in_schema=False)
async def course_js():
    body = "window.COURSE = " + json.dumps(public_course(), ensure_ascii=False) + ";\n" + PROGRESS_JS
    return Response(body, media_type="application/javascript", headers={"Cache-Control": "no-cache"})


class LoginData(BaseModel):
    username: str
    password: str


@app.post("/api/login")
async def login(data: LoginData, response: Response):
    user_ok = hmac.compare_digest(data.username.strip().lower().encode(), TEACHER_USER.encode())
    password_ok = hmac.compare_digest(data.password.encode(), TEACHER_PASSWORD.encode())
    if not (user_ok and password_ok):
        raise HTTPException(status_code=401, detail="Wrong username or password")
    response.set_cookie(SESSION_COOKIE, session_token(), max_age=60 * 60 * 24 * 30, httponly=True, samesite="lax")
    return {"teacher": True}


@app.post("/api/logout")
async def logout(response: Response):
    response.delete_cookie(SESSION_COOKIE)
    return {"teacher": False}


@app.get("/api/me")
async def me(request: Request):
    return {"teacher": is_teacher(request)}


@app.get("/api/answers/{lesson_id}")
async def answers(lesson_id: int, request: Request):
    if not is_teacher(request):
        raise HTTPException(status_code=403, detail="Teachers only")
    lesson = find_lesson(lesson_id)
    return {"answers": [teacher_answer(lesson_id, i) for i in range(len(lesson["tasks"]))], "tips": lesson.get("tips")}


# ---------------------------------------------------------------------------
# Expected results of the task kinds
#   "row"     - will employee <row> pass <condition>? The student answers yes or no.
#   "pick"    - the student marks every row that passes <condition>.
#   "value"   - what does <expr> return? The student answers true, false (or null).
#   "truth"   - a truth table: every combination of "vars", one column per "cols".
#   "rewrite" - the student writes a condition that means the same as <expr>, but in
#               another form ("form"). The browser works it out on every combination
#               of values and sends the result; here it is compared with the original.
# ---------------------------------------------------------------------------


def expected(lesson_id: int, task: int) -> dict:
    return RESULTS["lessons"][str(lesson_id)]["tasks"][find_lesson(lesson_id)["tasks"][task]["id"]]


def passing_rows(lesson_id: int, task: int) -> list[list]:
    """(id, name) of every row that passes the task's condition, on the original data."""
    return expected(lesson_id, task)["passing"]


def logic_value(lesson_id: int, task: int) -> str:
    return expected(lesson_id, task)["value"]


def truth_table(lesson_id: int, task: int) -> list[list[str]]:
    return expected(lesson_id, task)["table"]


REWRITE_FORMS = {
    "no_not_bracket": re.compile(r"\bnot\s*\(", re.I),   # De Morgan: no NOT in front of a bracket
    "no_not": re.compile(r"\bnot\b", re.I),               # comparisons: the opposite operator instead of NOT
}


def check_rewrite(lesson_id: int, task: int, expr: str, values: list | None) -> dict:
    t = find_lesson(lesson_id)["tasks"][task]
    expr = (expr or "").strip().rstrip(";").strip()
    want = expected(lesson_id, task)["original"]
    if not expr or ";" in expr or len(expr) > 500 or values is None or len(values) != len(want):
        return {"ok": False, "reason": "error"}
    if any(v not in (True, False, None) for v in values):      # not a condition
        return {"ok": False, "reason": "error"}
    differ = sum(1 for a, b in zip(want, values) if a != b)    # 1 == True and 0 == False here
    if differ:
        return {"ok": False, "reason": "differs", "rows": differ}
    form = REWRITE_FORMS.get(t.get("form", "no_not_bracket"))
    if form and form.search(re.sub(r"'(?:[^']|'')*'", "''", expr)):
        return {"ok": False, "reason": "form"}
    return {"ok": True, "explain": t.get("explain")}


def teacher_answer(lesson_id: int, task: int) -> str:
    t = find_lesson(lesson_id)["tasks"][task]
    if t.get("kind") == "value":
        return logic_value(lesson_id, task).upper()
    if t.get("kind") == "truth":
        table = truth_table(lesson_id, task)
        return "\n".join(f"{col}: " + ", ".join(row[j].upper() for row in table) for j, col in enumerate(t["cols"]))
    if t.get("kind") == "row":
        return "Yes" if t["row"] in [r[0] for r in passing_rows(lesson_id, task)] else "No"
    if t.get("kind") == "pick":
        rows = passing_rows(lesson_id, task)
        return ", ".join(f"{name} ({rid})" for rid, name in rows) or "nobody"
    return t["answer"]


def _normalize(value):
    if isinstance(value, float):
        value = round(value, 6)                # sums of fractions may differ in the last digits
        if value.is_integer():
            return int(value)
    return value


class CheckData(BaseModel):
    lesson: int
    task: int
    columns: list[str] = []
    rows: list[list] = []
    answer: str | None = None        # "row" tasks: "yes" or "no"; "value" tasks: "true", "false" or "null"; "rewrite" tasks: the condition
    values: list | None = None       # "rewrite" tasks: the condition's value on every combination
    picked: list[int] | None = None  # prediction "pick" tasks: the ids the student marked
    cells: list[list[str]] | None = None  # truth tables: "true" / "false" / "null" / "" per cell


# Rows that are equal in every ORDER BY column may come in any order, so the student's
# rows are compared group by group (the groups come from scripts/build_results.py).
def sorted_rows_match(order, got: list[str]) -> bool:
    start, size, groups, by_pos = order
    if len(got) != size:
        return False
    pools = [list(g) for g in groups]
    for i, row in enumerate(got):
        pool = pools[by_pos[start + i]]
        if row not in pool:
            return False
        pool.remove(row)
    return True


@app.post("/api/check")
async def check(data: CheckData):
    lesson = find_lesson(data.lesson)
    if not 0 <= data.task < len(lesson["tasks"]):
        raise HTTPException(status_code=404, detail="Task not found")
    task = lesson["tasks"][data.task]
    if task.get("kind") == "row":
        passes = task["row"] in [r[0] for r in passing_rows(data.lesson, data.task)]
        return {"ok": (data.answer == "yes") == passes, "explain": task.get("explain")}
    if task.get("kind") == "value":
        return {"ok": data.answer == logic_value(data.lesson, data.task), "explain": task.get("explain")}
    if task.get("kind") == "rewrite":
        return check_rewrite(data.lesson, data.task, data.answer, data.values)
    if task.get("kind") == "truth":
        want = truth_table(data.lesson, data.task)
        got = data.cells or []
        wrong = sum(1 for i, row in enumerate(want) for j, v in enumerate(row)
                    if i >= len(got) or j >= len(got[i]) or got[i][j] != v)
        return {"ok": wrong == 0, "wrong": wrong, "explain": task.get("explain")}
    if task.get("kind") == "pick":
        want = {r[0] for r in passing_rows(data.lesson, data.task)}
        got = set(data.picked or [])
        return {"ok": got == want, "wrong": len(want ^ got), "explain": task.get("explain")}
    want_result = expected(data.lesson, data.task)
    columns, rows = want_result["columns"], want_result["rows"]
    if lesson.get("check") == "values":        # business questions: any column names, the same columns in the same order
        if len(columns) != len(data.columns):
            return {"ok": False, "reason": "columns", "expected": columns}
    elif [c.lower() for c in columns] != [c.lower() for c in data.columns]:
        return {"ok": False, "reason": "columns", "expected": columns}
    if len(rows) != len(data.rows):
        return {"ok": False, "reason": "rows", "expected": len(rows)}
    got = [json.dumps([_normalize(v) for v in row]) for row in data.rows]
    want = [json.dumps(row) for row in rows]
    if "order" in want_result:
        if want_result["order"] is not None:   # rows that tie in the sort may come in any order
            return {"ok": True} if sorted_rows_match(want_result["order"], got) else {"ok": False, "reason": "values"}
    else:
        got.sort()
        want.sort()
    if got != want:
        return {"ok": False, "reason": "values"}
    return {"ok": True}


# ---------------------------------------------------------------------------
# Students' queries: each room has one database on PostgreSQL (pg_engine.py), and each student
# (a browser tab, `client`) has their own connection to it. These calls block on the database,
# so they run in a thread: one student waiting on another's lock holds up nobody else.
# ---------------------------------------------------------------------------
class DbClient(BaseModel):
    room: str = Field(min_length=1, max_length=100)
    client: str = Field(pattern=r"^[0-9a-f]{32}$")


class DbCall(DbClient):
    op: str
    sql: str = ""
    key: str = Field(default="", max_length=100)     # "open", "reset": which lesson's data
    lang: str = Field(default="en", max_length=10)   # "open", "reset": the language of that data


def db_action(call: DbCall):
    if call.op == "run":
        return pg_engine.run(call.room, call.client, call.sql)
    if call.op == "tables":
        return pg_engine.tables(call.room, call.client)
    if call.op in ("open", "reset"):
        return pg_engine.open_room(call.room, call.key, call.lang, call.sql, force=call.op == "reset")
    raise HTTPException(status_code=404, detail="Unknown operation")


@app.post("/api/db")
async def database(call: DbCall):
    try:
        result = await run_in_threadpool(db_action, call)
    except pg_engine.SessionLost:
        return JSONResponse({"error": {"message": "The database of this room is gone.", "lost": True}}, status_code=409)
    except pg_engine.EngineError as e:
        return JSONResponse({"error": e.info}, status_code=400)
    if call.op in ("open", "reset") and result["reset"]:
        await tell_room(call.room, json.dumps({"type": "db-reset", "client": call.client}))
    return {"result": result}


@app.post("/api/db/close")
def close_connection(call: DbClient):
    try:
        pg_engine.disconnect(call.room, call.client)
    except psycopg.Error:
        pass
    return Response(status_code=204)


@app.get("/healthz", include_in_schema=False)
async def healthz():
    """Used by Render to check that the service is up."""
    return {"status": "ok"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


# ---------------------------------------------------------------------------
# Real-time collaboration
#
# Each room is relayed by the server, separately for each page ("room~page"). All
# pages of a room share one database. A write runs once, on the connection of the
# student who pressed Run; the others receive the result and re-read the tables.
#   * binary frames are Yjs updates for the shared editor text: stored, so late
#     joiners get the current text, and forwarded to everyone else;
#   * {"type": "presence"} - a user's name, colour, editor cursor and selected
#     cells: the latest one per user is stored and forwarded;
#   * {"type": "pointer"} - mouse position: forwarded only;
#   * {"type": "page"} - shared navigation between pages (go to a URL, scroll,
#     pick a lesson): forwarded only, so a newcomer is never redirected;
#   * {"type": "event"} - a shared action (a query's result, switch sheet, lesson,
#     language). The server numbers it and sends it to EVERYONE, sender included,
#     so all browsers apply actions in the same order. Most also go to the room
#     log, which newcomers replay; NOT_REPLAYED ones are about a moment that has
#     passed, and a newcomer reads the database as it is now;
#   * {"type": "db-reset"} - comes from the server when the room's database was
#     reseeded, to every page of the room.
# Rooms live in memory and are dropped when the last person leaves. Their
# databases stay on PostgreSQL.
# ---------------------------------------------------------------------------
NOT_REPLAYED = {"run", "why"}


class Room:
    def __init__(self) -> None:
        self.epoch = uuid.uuid4().hex
        self.updates: list[bytes] = []
        self.log: list[dict] = []
        self.seq = 0
        self.clients: dict[WebSocket, dict] = {}  # ws -> {"cid": str, "presence": str | None}


rooms: dict[str, Room] = {}


async def broadcast(room: Room, message: bytes | str, exclude: WebSocket | None = None) -> None:
    for client in list(room.clients):
        if client is exclude:
            continue
        try:
            if isinstance(message, bytes):
                await client.send_bytes(message)
            else:
                await client.send_text(message)
        except Exception:
            room.clients.pop(client, None)


async def tell_room(room_id: str, message: str) -> None:
    """To every page of the room: the keys of `rooms` are "room~page"."""
    for name, room in list(rooms.items()):
        if name.rsplit("~", 1)[0] == room_id:
            await broadcast(room, message)


@app.websocket("/ws/{room_id}")
async def collaborate(ws: WebSocket, room_id: str, cid: str = ""):
    await ws.accept()
    room = rooms.setdefault(room_id, Room())
    room.clients[ws] = {"cid": cid, "presence": None}

    # Catch the newcomer up: editor text, everyone's cursors, then the action log.
    for update in list(room.updates):
        await ws.send_bytes(update)
    for other, info in list(room.clients.items()):
        if other is not ws and info["presence"]:
            await ws.send_text(info["presence"])
    await ws.send_text(json.dumps({"type": "synced", "epoch": room.epoch, "log": room.log}))

    try:
        while True:
            message = await ws.receive()
            if message["type"] == "websocket.disconnect":
                break
            if message.get("bytes"):
                room.updates.append(message["bytes"])
                await broadcast(room, message["bytes"], exclude=ws)
                continue
            text = message.get("text")
            if not text:
                continue
            try:
                data = json.loads(text)
            except ValueError:
                continue
            kind = data.get("type")
            if kind == "presence":
                room.clients[ws]["presence"] = text
                await broadcast(room, text, exclude=ws)
            elif kind in ("pointer", "page"):
                # mouse moves and page navigation (go to a page, scroll, ...): forwarded, never stored
                await broadcast(room, text, exclude=ws)
            elif kind == "event":
                room.seq += 1
                data["seq"] = room.seq
                if data.get("kind") not in NOT_REPLAYED:
                    room.log.append(data)
                await broadcast(room, json.dumps(data))
    except WebSocketDisconnect:
        pass
    finally:
        room.clients.pop(ws, None)
        if cid:
            await broadcast(room, json.dumps({"type": "leave", "cid": cid}))
        if not room.clients:
            rooms.pop(room_id, None)
