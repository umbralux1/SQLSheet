import hashlib
import hmac
import json
import os
import re
import secrets
import sqlite3
import uuid
from functools import lru_cache
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request, Response, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from pydantic import BaseModel

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
# results are checked on the server (/api/check); only the logged-in teacher
# can read the answers (/api/answers/<lesson id>).
#
# Teacher login: user "teacher", password from the TEACHER_PASSWORD environment
# variable (default "sql2026" - change it on Render).
# ---------------------------------------------------------------------------

TEACHER_USER = "teacher"
TEACHER_PASSWORD = os.environ.get("TEACHER_PASSWORD", "sql2026")
SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_hex(32)  # a random key logs everyone out on restart
SESSION_COOKIE = "sqlt_teacher"

PROGRESS_JS = """
/* Progress is kept per browser, as a list of solved task ids ("2.10", "2.or3", ...).
   Older versions saved task positions (0, 1, 2, ...). Task ids were numbered from
   those positions, so position n is task "<lesson>.<n+1>" and old progress carries over. */
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
    lessons = []
    for lesson in COURSE["lessons"]:
        item = {k: v for k, v in lesson.items() if k not in ("tasks", "tips")}
        if "tasks" in lesson:
            item["tasks"] = [{k: v for k, v in t.items() if k not in ("answer", "explain")} for t in lesson["tasks"]]
        lessons.append(item)
    return {"lessons": lessons}


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
# Prediction tasks
#   "kind": "row"  - will employee <row> pass <condition>? The student answers yes or no.
#   "kind": "pick" - the student marks every row that passes <condition>.
# Rows are identified by the first column of the lesson's first table (emp_id).
# ---------------------------------------------------------------------------


@lru_cache(maxsize=256)
def passing_rows(lesson_id: int, task: int) -> tuple[tuple, ...]:
    """(id, name) of every row that passes the task's condition, on the original data."""
    lesson = find_lesson(lesson_id)
    t = lesson["tasks"][task]
    table = t.get("table", lesson["tables"][0])
    con = sqlite3.connect(":memory:")
    try:
        con.executescript(lesson["seed"])
        rows = con.execute(f'SELECT * FROM "{table}" WHERE {t["condition"]}').fetchall()
    finally:
        con.close()
    return tuple((r[0], r[1]) for r in rows)


def teacher_answer(lesson_id: int, task: int) -> str:
    t = find_lesson(lesson_id)["tasks"][task]
    if t.get("kind") == "row":
        return "Yes" if t["row"] in [r[0] for r in passing_rows(lesson_id, task)] else "No"
    if t.get("kind") == "pick":
        rows = passing_rows(lesson_id, task)
        return ", ".join(f"{name} ({rid})" for rid, name in rows) or "nobody"
    return t["answer"]


def _normalize(value):
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value


@lru_cache(maxsize=256)
def expected_result(lesson_id: int, task: int) -> tuple[list[str], list[list]]:
    lesson = find_lesson(lesson_id)
    con = sqlite3.connect(":memory:")
    try:
        con.executescript(lesson["seed"])
        cur = con.execute(lesson["tasks"][task]["answer"])
        columns = [d[0] for d in cur.description or []]
        rows = [[_normalize(v) for v in row] for row in cur.fetchall()]
    finally:
        con.close()
    return columns, rows


class CheckData(BaseModel):
    lesson: int
    task: int
    columns: list[str] = []
    rows: list[list] = []
    answer: str | None = None        # prediction "row" tasks: "yes" or "no"
    picked: list[int] | None = None  # prediction "pick" tasks: the ids the student marked


@app.post("/api/check")
async def check(data: CheckData):
    lesson = find_lesson(data.lesson)
    if not 0 <= data.task < len(lesson["tasks"]):
        raise HTTPException(status_code=404, detail="Task not found")
    task = lesson["tasks"][data.task]
    if task.get("kind") == "row":
        passes = task["row"] in [r[0] for r in passing_rows(data.lesson, data.task)]
        return {"ok": (data.answer == "yes") == passes, "explain": task.get("explain")}
    if task.get("kind") == "pick":
        want = {r[0] for r in passing_rows(data.lesson, data.task)}
        got = set(data.picked or [])
        return {"ok": got == want, "wrong": len(want ^ got), "explain": task.get("explain")}
    columns, rows = expected_result(data.lesson, data.task)
    if [c.lower() for c in columns] != [c.lower() for c in data.columns]:
        return {"ok": False, "reason": "columns", "expected": columns}
    if len(rows) != len(data.rows):
        return {"ok": False, "reason": "rows", "expected": len(rows)}
    got = [json.dumps([_normalize(v) for v in row]) for row in data.rows]
    want = [json.dumps(row) for row in rows]
    if not re.search(r"\border\s+by\b", lesson["tasks"][data.task]["answer"], re.I):
        got.sort()
        want.sort()
    if got != want:
        return {"ok": False, "reason": "values"}
    return {"ok": True}


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
# Each room is relayed by the server; the real work happens in the browsers.
#   * binary frames are Yjs updates for the shared editor text: stored, so late
#     joiners get the current text, and forwarded to everyone else;
#   * {"type": "presence"} - a user's name, colour, editor cursor and selected
#     cells: the latest one per user is stored and forwarded;
#   * {"type": "pointer"} - mouse position: forwarded only;
#   * {"type": "page"} - shared navigation between pages (go to a URL, scroll,
#     pick a lesson): forwarded only, so a newcomer is never redirected;
#   * {"type": "event"} - a shared action (run a query, reset the database,
#     switch sheet, lesson, language, semicolon mode). The server numbers it,
#     appends it to the room log and sends it to EVERYONE, sender included,
#     so all browsers apply actions in the same order and keep identical
#     databases. Newcomers replay the log.
# Rooms live in memory and are dropped when the last person leaves.
# ---------------------------------------------------------------------------


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
