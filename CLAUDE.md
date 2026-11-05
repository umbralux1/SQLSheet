# SQL Sheet

SQL trainer. Students' queries run on a real PostgreSQL server. Commands: `make`. Overview: `README.md`.

## Architecture: one PostgreSQL server, one database per room

Moved from PGlite to a server on 2026-11-05: the course is for two people, and it needs real PostgreSQL with several connections for concurrency lessons. Results on Postgres 18.6 matched PGlite's value for value.

- **Engine seam.** Pages reach the database only through `static/pg-engine.js` (`open`, `reset`, `run`, `tables`), which calls `/api/db` with the room and the page's `client` id.
- **Shared result format.** `pg_engine.py` serves both `main.py` and `scripts/build_results.py`, so a student's rows and the expected rows always match in format. Change value conversion only there, then run `make results`.
- **Isolation.** `DATABASE_ADMIN_URL` only creates roles and databases and ends connections on a reseed. Each room's database belongs to `sheet_student`, which has no special rights. Databases are named `sheet_<hash>_<created>`, survive server restarts, and are dropped only by the sweep (nobody connected, and older than 24 h or more than 30 databases).
- **Rooms.** One database per room, one connection per student (browser tab), so transactions, locks and settings are each student's own. Progress lives only in the browser (`localStorage`), so the database is disposable: this is a requirement from the user.
- **A write runs once.** `userRun()` runs the query on the student's connection, then `announceRun` sends the outcome as a `run` event; the others pass it to `run(src, {...outcome, remote: true})`, which runs nothing, and re-read tables on their own connections. Queries the page generates by itself (`revealResult`, `truthExpected`, "Explain") only read, so each browser runs its own.
- **Reseeding.** `open` keeps data if the database's comment names the same lesson (`key`), otherwise it reseeds; `reset` always does. A reseed ends all the room's connections, because an open transaction would block it, then the server sends `db-reset` to every page of the room. The WebSocket room is still `room~page`, for editor text and task state. Newcomers replay the log without `run` and `why`, and read the data from the database.
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

The repo has no automated tests. `make db` starts PostgreSQL. `make check` checks structure and that results are fresh; `make results` runs all SQL. To exercise the real path, run each task's answer in the browser through `db.run` and POST it to `/api/check`, with answers from `/api/answers/<id>` after a teacher login. All 285 tasks passed this way with one database per room on 2026-11-05. Reset between tasks with `db.reset`: answers can change data. For room behaviour, open two tabs on the same `?room=`. Clear `sqlt-*` keys from `localStorage` afterwards.

## Open as of 2026-11-05

- Production is not deployed yet. Decision: Render free for both the app and the database, described in `render.yaml` (Frankfurt, PostgreSQL 18, internal connections only). The free database expires after 30 days and must be recreated by hand; this is accepted because the database is disposable. The code needs an admin account with `CREATEDB` and `CREATEROLE`: tested on a local server with such a non-superuser role (seed, reseed with an open transaction, all course SQL), but Render's docs do not state its default account's rights, so the first deploy has to confirm them.
- The site has no login for students: anyone with its address can run SQL as `sheet_student`. A shared password was suggested and not decided. All rooms use that one role, so a student can also end other rooms' connections with `pg_terminate_backend`.
- Concurrency lessons (locks, isolation levels) are not built yet. The page shows nothing while a query waits on another student's lock (up to 20 s), and `tables()` on the waiting side can wait too.
- Branch `feat/pglite` is merged and can be deleted.
