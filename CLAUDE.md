# SQL Sheet

SQL trainer. Students' queries run on real PostgreSQL in the browser (PGlite, WebAssembly). Commands: `make`. Overview: `README.md`.

## Architecture: PostgreSQL only in the browser

Moved from SQLite (sql.js) to PGlite on 2026-11-05 (commit `90bfb90`), because the course should teach PostgreSQL without running a database server.

- **Engine seam.** Pages reach the database only through `static/pg-engine.js` (`run`, `reset`, `tables`). The planned server-backed engine for concurrency lessons implements these same methods.
- **Shared result format.** `static/pg-core.js` runs in both the browser worker and `scripts/pg_bridge.mjs`, so a student's rows and the expected rows always match in format. Change value conversion only there, then run `make results`.
- **Server has no database.** `/api/check` compares against `course_results.json`, because Python cannot run PGlite and Render has no Node. Students never receive answers; the file is read on the server, and only `previews` and `examples` go to `/course.js`.
- **Lessons page** draws tables and examples from those results and loads no WASM.

## Rules

- After changing a lesson's data, answers, examples or conditions: `make results`, then commit `course_results.json` with `course.py`.
- Task `id`s stay stable when a task is rewritten: saved progress and collaboration use them.
- The PGlite version in `package.json` and `static/pg-worker.js` stays identical.
- Lesson text comes in `en` and `ru`, and describes PostgreSQL behaviour.

## Frontend conventions (`static/index.html`)

- **`serial()`** gives every database action a turn, which keeps databases identical across a collaboration room. Wrap entry points (buttons, shared events) in it. A step already in its turn calls the next step directly and awaits it; going through `serial()` from inside a turn deadlocks.
- **`tableData`** is a copy of all tables, refreshed after each query, so drawing stays synchronous. Read it through `tables()`, `tableInfo()`, `tableOf()`.
- Boolean values in generated SQL use `sqlBool`: a bare `NULL` has no type in PostgreSQL.

## PGlite gotchas

- `statement_timeout` has no effect. `PgEngine` stops a long query by terminating the worker after 20 s, which loses the data, so the caller reseeds (`e.timedOut`).
- `affectedRows` accumulates across a multi-statement `exec`; `runSql` takes the difference.
- `numeric` becomes a JS number: `2.50` shows as `2.5`, and very long values lose precision.
- `rewrite` tasks: the browser computes the condition's values and the server compares them, so a student could fake them, as with ordinary task results.

## Verifying a change

The repo has no automated tests. `make check` checks structure and that results are fresh; `make results` runs all SQL. To exercise the real path, run each task's answer in the browser through `db.run` and POST it to `/api/check`, with answers from `/api/answers/<id>` after a teacher login. All 285 tasks passed this way on 2026-11-05. Clear `sqlt-*` keys from `localStorage` afterwards.

## Open as of 2026-11-05

- Pushed to `main`, but the Render deploy is unconfirmed: the site's address is unknown (`sql-sheet.onrender.com` returns 404). Ask the user for it.
- First load from an empty cache and phones are unmeasured (about 15 MB before compression; about 1.2 s to start with the engine cached).
- Concurrency lessons (locks, isolation levels) need several connections, which PGlite lacks. Decision: most lessons stay on PGlite, and those lessons get a separate real PostgreSQL. Not built yet.
- Branch `feat/pglite` is merged and can be deleted.
