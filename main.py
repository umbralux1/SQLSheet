import json
import uuid
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="SQL Sheet")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
async def root():
    """Home page: the SQL trainer with an Excel-style result grid."""
    return FileResponse(STATIC_DIR / "index.html")


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
            elif kind == "pointer":
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
