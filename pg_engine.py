"""Runs SQL on the real PostgreSQL server. Used by main.py (students) and scripts/build_results.py
(expected results), so a student's rows and the expected rows always come out in the same format.
Change value conversion only here, then run `make results`.

Every collaboration room has one database, owned by one low-privilege role, and every student (a
browser tab) in the room has their own connection to it, so one student's open transaction is not
another's. The address of the server comes from DATABASE_ADMIN_URL; that account only creates and
drops the databases and ends connections when a room is reseeded.

Databases outlive this process, because a free Render service restarts whenever it wakes up. A
student reconnects after that; their open transaction and settings are gone. Nothing of the
student's lives only here: progress is kept in the browser, so a database can always be reseeded.
"""
import hashlib
import json
import os
import re
import threading
import time

import psycopg
from psycopg import conninfo, sql as pgsql
from psycopg.pq import ExecStatus

STUDENT_ROLE = "sheet_student"
PREFIX = "sheet_"
STATEMENT_TIMEOUT_S = 20
HARD_LIMIT_S = STATEMENT_TIMEOUT_S + 5       # a student can turn statement_timeout off
ROW_LIMIT = 5000                             # rows of each table sent to the sheets
MAX_AGE_S = 24 * 60 * 60                     # a room nobody is connected to
MAX_DATABASES = 30
IDLE_CLOSE_S = 10 * 60                       # lets a hosted server suspend; the database stays
PING_AFTER_S = 60                            # a suspended server has dropped the connection


class EngineError(Exception):
    """A PostgreSQL error, in the form the page shows it."""

    def __init__(self, message, hint=None, code=None, position=None):
        super().__init__(message)
        self.info = {"message": message, "hint": hint, "code": code, "position": position}


class SessionLost(Exception):
    """The room's database is gone. The page starts again from the seed."""


def _admin_url() -> str:
    url = os.environ.get("DATABASE_ADMIN_URL")
    if not url:
        raise EngineError("DATABASE_ADMIN_URL is not set. Locally: make db")
    return url


def _student_password() -> str:
    """Stable, so the server and `make results` can share one PostgreSQL."""
    return hashlib.sha256(("sql-sheet:" + _admin_url()).encode()).hexdigest()


def _connect(url: str, **overrides) -> psycopg.Connection:
    # prepare_threshold=None: psycopg must never prepare a student's multi-statement text.
    return psycopg.connect(conninfo.make_conninfo(url, **overrides), autocommit=True, prepare_threshold=None)


# ---------------------------------------------------------------------------
# Values arrive as JSON-friendly data: dates and JSON stay text as PostgreSQL prints them,
# numeric and bigint become plain numbers (a value too big for that stays text).
# ---------------------------------------------------------------------------
MAX_SAFE_INTEGER = 2 ** 53 - 1


def _integer(text: str):
    value = int(text)
    return value if abs(value) <= MAX_SAFE_INTEGER else text


def _number(text: str):
    value = float(text)
    if value - value != 0:                            # NaN and Infinity stay text: JSON has neither
        return text
    return int(value) if value.is_integer() and abs(value) <= MAX_SAFE_INTEGER else value


_CONVERT = {
    16: lambda text: text == "t",                     # boolean
    20: _integer,                                     # bigint
    21: int, 23: int, 26: int,                        # smallint, integer, oid
    700: _number, 701: _number, 1700: _number,        # real, double precision, numeric
}


def _rows(result) -> list[list]:
    convert = [_CONVERT.get(result.ftype(c)) for c in range(result.nfields)]
    rows = []
    for r in range(result.ntuples):
        row = []
        for c, to_value in enumerate(convert):
            raw = result.get_value(r, c)
            if raw is None:
                row.append(None)
                continue
            text = raw.decode("utf-8", "replace")
            row.append(to_value(text) if to_value else text)
        rows.append(row)
    return rows


def _affected(result) -> int:
    words = (result.command_status or b"").decode().split()
    return int(words[-1]) if words and words[0] in ("INSERT", "UPDATE", "DELETE", "MERGE") else 0


def _error_info(e: psycopg.Error) -> EngineError:
    d = e.diag
    position = int(d.statement_position) if d.statement_position else None
    return EngineError(d.message_primary or str(e), d.message_hint, d.sqlstate, position)


def run_sql(conn: psycopg.Connection, text: str) -> list[dict]:
    """Runs one or more statements. One result per statement: {columns, rows, returnsRows, affected}.
    All of them run as one transaction, as PostgreSQL does for one simple query."""
    results = []
    try:
        with conn.cursor() as cur:
            cur.execute(text)
            while True:
                result = cur.pgresult
                if result is not None and result.status != ExecStatus.EMPTY_QUERY:
                    results.append({
                        "columns": [result.fname(c).decode() for c in range(result.nfields)],
                        "rows": _rows(result),
                        "returnsRows": result.nfields > 0,
                        "affected": _affected(result),
                    })
                if not cur.nextset():
                    return results
    except psycopg.Error as e:
        if conn.closed or conn.broken:            # not the student's mistake: _call deals with it
            raise
        if isinstance(e, psycopg.ProgrammingError) and "empty query" in str(e):   # only spaces or comments
            return results
        raise _error_info(e) from e


def clear_database(conn: psycopg.Connection) -> None:
    """Back to an empty database, whatever the student did: open transaction, settings, schemas."""
    run_sql(conn, "ROLLBACK")
    run_sql(conn, "DISCARD ALL")
    schemas = run_sql(conn, "SELECT nspname FROM pg_namespace "
                            r"WHERE nspname NOT LIKE 'pg\_%' AND nspname <> 'information_schema'")[0]["rows"]
    drops = " ".join('DROP SCHEMA "{}" CASCADE;'.format(s[0].replace('"', '""')) for s in schemas)
    run_sql(conn, drops + " CREATE SCHEMA public;")


def read_tables(conn: psycopg.Connection) -> list[dict]:
    """Every table of the public schema, in the order they were created. Shown as sheets and in the
    sidebar. pk marks the primary key's columns: rows are sorted by it, and it tells which row
    changed. Without one, a row is known by its whole content."""
    columns = run_sql(conn, """
        SELECT c.relname, a.attname, format_type(a.atttypid, a.atttypmod),
               a.attnum = ANY(COALESCE(i.indkey::int2[], '{}'))
        FROM pg_class c
        JOIN pg_namespace n ON n.oid = c.relnamespace
        JOIN pg_attribute a ON a.attrelid = c.oid AND a.attnum > 0 AND NOT a.attisdropped
        LEFT JOIN pg_index i ON i.indrelid = c.oid AND i.indisprimary
        WHERE n.nspname = 'public' AND c.relkind IN ('r', 'p')
        ORDER BY c.oid, a.attnum""")[0]["rows"]
    tables: list[dict] = []
    for table, name, type_name, pk in columns:
        if not tables or tables[-1]["name"] != table:
            tables.append({"name": table, "columns": []})
        tables[-1]["columns"].append({"name": name, "type": type_name.replace("character varying", "varchar"), "pk": pk})

    def quote(name: str) -> str:
        return '"' + name.replace('"', '""') + '"'

    for t in tables:
        key = ", ".join(quote(c["name"]) for c in t["columns"] if c["pk"])
        count, data = run_sql(conn, f"SELECT count(*) FROM {quote(t['name'])}; "
                                    f"SELECT * FROM {quote(t['name'])} ORDER BY {key or 'ctid'} LIMIT {ROW_LIMIT};")
        t["count"] = count["rows"][0][0]
        t["rows"] = data["rows"]
    return tables


# ---------------------------------------------------------------------------
# Rooms: one database per room, one connection per student
# ---------------------------------------------------------------------------
class _Room:
    def __init__(self, database: str) -> None:
        self.database = database
        self.lock = threading.Lock()         # held while reseeding: nobody connects meanwhile
        self.epoch = object()                # replaced by a reseed, which ends every connection


class _Student:
    def __init__(self, room: _Room, conn: psycopg.Connection) -> None:
        self.room = room
        self.epoch = room.epoch
        self.conn = conn
        self.lock = threading.Lock()         # one action at a time on this connection
        self.used = time.monotonic()


_rooms: dict[str, _Room] = {}
_students: dict[tuple[str, str], _Student] = {}
_registry_lock = threading.Lock()
_role_ready = False


def _ensure_role(admin: psycopg.Connection) -> None:
    global _role_ready
    if _role_ready:
        return
    role, password = pgsql.Identifier(STUDENT_ROLE), pgsql.Literal(_student_password())
    exists = admin.execute("SELECT 1 FROM pg_roles WHERE rolname = %s", [STUDENT_ROLE]).fetchone()
    if not exists:
        admin.execute(pgsql.SQL("CREATE ROLE {} LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE PASSWORD {}").format(role, password))
    else:
        admin.execute(pgsql.SQL("ALTER ROLE {} PASSWORD {}").format(role, password))
    admin.execute(pgsql.SQL("ALTER ROLE {} SET statement_timeout = {}").format(role, pgsql.Literal(f"{STATEMENT_TIMEOUT_S}s")))
    # Creating a database owned by the role needs membership; on a superuser this changes nothing.
    admin.execute(pgsql.SQL("GRANT {} TO CURRENT_USER").format(role))
    _role_ready = True


def _db_prefix(room_id: str) -> str:
    return f"{PREFIX}{hashlib.sha256(room_id.encode()).hexdigest()[:24]}_"


def _find_database(admin: psycopg.Connection, room_id: str) -> str | None:
    row = admin.execute("SELECT datname FROM pg_database WHERE starts_with(datname, %s)", [_db_prefix(room_id)]).fetchone()
    return row[0] if row else None


def _sweep(admin: psycopg.Connection) -> None:
    """Drops old databases of rooms nobody is connected to, and connections nobody is using.
    This is the only thing that removes a room's database: leaving a room keeps it, so a reload
    or a returning student finds the data."""
    now = time.monotonic()
    for key, s in list(_students.items()):
        if now - s.used > IDLE_CLOSE_S and s.lock.acquire(blocking=False):
            try:
                s.conn.close()
                del _students[key]
            finally:
                s.lock.release()
    active = {s.room.database for s in _students.values()}
    for room_id, room in list(_rooms.items()):
        if room.database not in active:
            del _rooms[room_id]
    names = [r[0] for r in admin.execute("SELECT datname FROM pg_database WHERE starts_with(datname, %s)", [PREFIX])]
    created = {}
    for name in names:
        match = re.fullmatch(rf"{PREFIX}[0-9a-f]+_(\d+)", name)
        if match and name not in active:
            created[name] = int(match.group(1))
    oldest_first = sorted(created, key=created.get)
    surplus = max(0, len(names) - MAX_DATABASES + 1)
    for i, name in enumerate(oldest_first):
        if i < surplus or time.time() - created[name] > MAX_AGE_S:
            admin.execute(pgsql.SQL("DROP DATABASE IF EXISTS {} WITH (FORCE)").format(pgsql.Identifier(name)))


def _room(room_id: str, create: bool) -> _Room:
    """create=True always asks the server, so a database that disappeared is made again."""
    with _registry_lock:
        room = _rooms.get(room_id)
        if room and not create:
            return room
        with _connect(_admin_url()) as admin:
            _ensure_role(admin)
            database = _find_database(admin, room_id)
            if not database:
                if not create:
                    raise SessionLost
                _sweep(admin)
                database = f"{_db_prefix(room_id)}{int(time.time())}"
                # The builtin locale sorts by code point on every host, so results do not depend on the OS.
                admin.execute(pgsql.SQL("CREATE DATABASE {} OWNER {} TEMPLATE template0 ENCODING 'UTF8' "
                                        "LOCALE_PROVIDER builtin BUILTIN_LOCALE 'C.UTF-8' LOCALE 'C'")
                              .format(pgsql.Identifier(database), pgsql.Identifier(STUDENT_ROLE)))
        if room and room.database == database:
            return room
        room = _rooms[room_id] = _Room(database)
        return room


def _connect_student(database: str) -> psycopg.Connection:
    return _connect(_admin_url(), dbname=database, user=STUDENT_ROLE, password=_student_password())


def _student(room_id: str, client: str) -> _Student:
    room = _room(room_id, False)
    key = (room_id, client)
    with room.lock:                                         # waits for a reseed to finish
        with _registry_lock:
            student = _students.get(key)
            if student and student.room is room and student.epoch is room.epoch:
                return student
            _students.pop(key, None)
        if student:
            student.conn.close()
        conn = _connect_student(room.database)
        with _registry_lock:
            student = _students[key] = _Student(room, conn)
        return student


def _call(room_id: str, client: str, work):
    """One action on this student's connection, one at a time, on a connection known to be alive."""
    try:
        try:
            student = _student(room_id, client)
        except psycopg.OperationalError:
            with _registry_lock:
                _rooms.pop(room_id, None)                   # its database may be gone: ask the server
            student = _student(room_id, client)
    except psycopg.OperationalError as e:
        raise EngineError("Could not reach the database server. Try again in a moment.") from e
    with student.lock:
        conn = student.conn
        if conn.closed or time.monotonic() - student.used > PING_AFTER_S:
            try:
                conn.execute("SELECT 1")
            except psycopg.Error:
                if conn.closed or conn.broken:
                    _forget(room_id, client, conn)
                    return _call(room_id, client, work)     # nothing of the student's has run yet
                # otherwise inside a failed transaction: alive
        student.used = time.monotonic()
        try:
            return work(conn)
        except psycopg.Error as e:
            _forget(room_id, client, conn)                  # run_sql lets only a broken connection through
            raise EngineError("The connection to the database was lost. Run the query again.") from e
        finally:
            student.used = time.monotonic()


def _forget(room_id: str, client: str, conn: psycopg.Connection) -> None:
    with _registry_lock:
        _students.pop((room_id, client), None)
    conn.close()


def run(room_id: str, client: str, text: str) -> list[dict]:
    def work(conn):
        watchdog = threading.Timer(HARD_LIMIT_S, conn.cancel)
        watchdog.start()
        try:
            return run_sql(conn, text)
        finally:
            watchdog.cancel()
    return _call(room_id, client, work)


def tables(room_id: str, client: str) -> list[dict]:
    return _call(room_id, client, read_tables)


def open_room(room_id: str, key: str, lang: str, seed: str, force: bool = False) -> dict:
    """Makes the room's database hold the lesson called `key`. Data stays when it already does, so
    joining or reloading changes nothing; another lesson, or force, reseeds it for everyone in the
    room: every connection ends, and with it every open transaction. A reseed needs them gone,
    because an open transaction would keep it waiting on its locks.

    The lesson and the language of the data are kept as a comment on the database, so they survive
    a server restart. Returns {"lang": language of the data, "reset": whether it was reseeded}."""
    try:
        room = _room(room_id, True)
        with room.lock, _connect(_admin_url()) as admin:
            database = pgsql.Identifier(room.database)
            comment = admin.execute("SELECT shobj_description(oid, 'pg_database') FROM pg_database WHERE datname = %s",
                                    [room.database]).fetchone()
            holds = json.loads(comment[0]) if comment and comment[0] else None
            if holds and holds["key"] == key and not force:
                return {"lang": holds["lang"], "reset": False}
            room.epoch = object()
            admin.execute("SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = %s", [room.database])
            admin.execute(pgsql.SQL("COMMENT ON DATABASE {} IS NULL").format(database))     # a failed seed is not a seeded room
            with _connect_student(room.database) as conn:
                clear_database(conn)
                run_sql(conn, seed)
            admin.execute(pgsql.SQL("COMMENT ON DATABASE {} IS {}")
                          .format(database, pgsql.Literal(json.dumps({"key": key, "lang": lang}))))
            return {"lang": lang, "reset": True}
    except psycopg.Error as e:
        raise EngineError("Could not reach the database server. Try again in a moment.") from e


def disconnect(room_id: str, client: str) -> None:
    """The student left: their connection ends, and any open transaction rolls back. The database
    stays for the others and for a reload; only the sweep removes it."""
    with _registry_lock:
        student = _students.pop((room_id, client), None)
    if not student:
        return
    try:
        student.conn.cancel()                               # a query may be waiting on a lock
    except psycopg.Error:
        pass
    with student.lock:
        student.conn.close()


def drop_room(room_id: str) -> None:
    """For scripts/build_results.py, which needs its database only while it runs."""
    with _registry_lock:
        _rooms.pop(room_id, None)
        for key in [k for k in _students if k[0] == room_id]:
            _students.pop(key).conn.close()
        with _connect(_admin_url()) as admin:
            database = _find_database(admin, room_id)
            if database:
                admin.execute(pgsql.SQL("DROP DATABASE IF EXISTS {} WITH (FORCE)").format(pgsql.Identifier(database)))
