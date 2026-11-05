# SQL Sheet

SQL trainer. Students' queries run on a real PostgreSQL server. Commands: `make`. Overview: `README.md`.

## Architecture: one PostgreSQL server, one database per tab

Moved from PGlite to a server on 2026-11-05: the course is for two people, and it needs real PostgreSQL with several connections for concurrency lessons. Results on Postgres 18.6 matched PGlite's value for value.

- **Engine seam.** Pages reach the database only through `static/pg-engine.js` (`run`, `reset`, `tables`), which calls `/api/db/<session>`.
- **Shared result format.** `pg_engine.py` serves both `main.py` and `scripts/build_results.py`, so a student's rows and the expected rows always match in format. Change value conversion only there, then run `make results`.
- **Isolation.** `DATABASE_ADMIN_URL` only creates roles and databases. Each tab's database belongs to `sheet_student`, which has no special rights. Databases are named `sheet_<hash>_<created>`, survive server restarts, and are dropped when the tab closes or by the sweep (older than 24 h, more than 30).
- **Rooms.** Each participant keeps a separate database; the room's action log keeps them identical. Concurrency lessons will need participants to share one database.
- **Checking.** `/api/check` compares against `course_results.json`. Students never receive answers; the file is read on the server, and only `previews` and `examples` go to `/course.js`.
- **Lessons page** draws tables and examples from those results and runs no queries.

## Rules

- After changing a lesson's data, answers, examples or conditions: `make results`, then commit `course_results.json` with `course.py`.
- Task `id`s stay stable when a task is rewritten: saved progress and collaboration use them.
- The PostgreSQL major version stays 18 in `docker-compose.yml` and in production; `course_results.json` is worked out on it.
- Lesson text comes in `en` and `ru`, and describes PostgreSQL behaviour.

## Frontend conventions (`static/index.html`)

- **`serial()`** gives every database action a turn, which keeps databases identical across a collaboration room. Wrap entry points (buttons, shared events) in it. A step already in its turn calls the next step directly and awaits it; going through `serial()` from inside a turn deadlocks.
- **`tableData`** is a copy of all tables, refreshed after each query, so drawing stays synchronous. Read it through `tables()`, `tableInfo()`, `tableOf()`.
- Boolean values in generated SQL use `sqlBool`: a bare `NULL` has no type in PostgreSQL.

## Engine gotchas

- psycopg counts `QueryCanceled` as `OperationalError`. A broken connection is told apart by `conn.broken`, not by the exception class.
- `make check` uses system Python with no packages, so `build_results.py` imports `pg_engine` only inside `Pg`.
- `numeric` becomes a number: `2.50` shows as `2.5`, and very long values lose precision. `bigint` above 2^53 stays text.
- Query results are read into server memory with no row limit, so a huge `SELECT` can run a small server out of memory.
- `rewrite` tasks: the browser computes the condition's values and the server compares them, so a student could fake them, as with ordinary task results.

## Verifying a change

The repo has no automated tests. `make db` starts PostgreSQL. `make check` checks structure and that results are fresh; `make results` runs all SQL. To exercise the real path, run each task's answer in the browser through `db.run` and POST it to `/api/check`, with answers from `/api/answers/<id>` after a teacher login. All 285 tasks passed this way on the server engine on 2026-11-05. Clear `sqlt-*` keys from `localStorage` afterwards.

## Open as of 2026-11-05

- Production is not set up. Plan: Render free for the app, Neon free for the database (`DATABASE_ADMIN_URL`). Neither has been tried with this code; measure Neon's wake-up time and `CREATE DATABASE` time.
- The site has no login for students: anyone with its address can run SQL as `sheet_student`.
- After a server restart, a room's participants can end up with different databases: the first to reconnect logs `init`, and the others rebuild from that log.
- Concurrency lessons (locks, isolation levels) are not built yet.
- Branch `feat/pglite` is merged and can be deleted.
