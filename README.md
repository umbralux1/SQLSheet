# SQL Sheet

**English** · [Русский](#русский)

An SQL trainer that runs students' queries on a real PostgreSQL server and shows
query results as a spreadsheet: column letters, row numbers, a formula bar,
sum/average/count for the selection, and highlighting of inserted and updated rows.

The interface, lessons and sample database are available in English (default) and
Russian. Switch with the EN / RU buttons in the top right; the choice is remembered.
Switching the language reloads the sample database in that language.

## Commands

Everything is in the `Makefile`; run `make` to see the list.

| Command | What it does |
|---|---|
| `make install` | Create `venv/` and install the dependencies |
| `make db` | Start PostgreSQL locally in Docker (needed by `make run` and `make results`) |
| `make run` | Start locally with auto-reload on http://127.0.0.1:8001 (`PORT=8002 make run` for another port) |
| `make run-lan` | Start for other computers on your network and print the address to share |
| `make start` | Start like Render does, without reload |
| `make open` | Open the trainer and the lessons page in the browser |
| `make results` | After changing a lesson: run all its SQL on PostgreSQL and save the expected results to `course_results.json`; commit that file |
| `make check` | Check the code and the lessons, that `course_results.json` is up to date, and that answers stay hidden |
| `make deploy` | Run the checks, refuse if something is not committed, then push to GitHub; Render deploys from there |
| `make deploy-hook` | Ask Render to redeploy right away (`RENDER_DEPLOY_HOOK=<url> make deploy-hook`) |
| `make status` | Show uncommitted files and commits not pushed yet |
| `make clean` | Remove Python caches |

## Run

```bash
make db     # PostgreSQL 18 in Docker
make run    # http://127.0.0.1:8001/
```

The app finds PostgreSQL through `DATABASE_ADMIN_URL`; the `Makefile` points it at the local
container. That account must be able to create roles and databases. Every room gets one database,
owned by the low-privilege role `sheet_student`, so students cannot read server files or create
roles. Pages reach the database only through `static/pg-engine.js`, which calls `/api/db`.
A query stops after 20 seconds. Results are checked against `course_results.json`.

## Structure

- `main.py` — FastAPI app, serves the page at `/`
- `static/index.html` — the whole trainer (HTML + CSS + JS)
- Translations (`T`), sample data (`SEED`) and lessons (`LESSONS`) are at the top of the `<script>` in `index.html`

## Lessons

`/lessons` is the course page: a roadmap of 13 topics, and for each ready lesson
the theory, its tables, tasks and answers for teachers. **Solve** opens the trainer
with that lesson's database (`/?lesson=1&task=3`); after **Run** the result is
checked against the reference answer. Progress is saved in the browser.

All course content lives in `course.py`. To add a lesson, fill in its
`theory`, `seed`, `tables` and `tasks` (each task needs an `answer` query) and set
`available: true`.

**After any change to a lesson's data, answers, examples or conditions:**

1. Run `make results`. It runs all the course's SQL on PostgreSQL and rewrites
   `course_results.json`. If a query fails, it names the task and does not write the file.
2. Commit `course_results.json` together with `course.py`. The server checks students'
   results against this file, so without it they would be checked against the old answers.

If you forget, `make check` fails with "run `make results`", and so does `make deploy`,
because it runs the check first. Changes to texts alone do not need this.

### Teacher account

Answers are visible only to the teacher: log in at the bottom of a lesson on
`/lessons` with the user **teacher**. The password comes from the
`TEACHER_PASSWORD` environment variable; without it the default is `sql2026`,
so set your own on Render (**Environment → Add variable**). Answers never reach
students' browsers: the trainer sends a student's result to `/api/check` and the
server compares it with the answer.

## Working together

Two or more people work on the same page in real time. Everything is shared:
the query text as it is typed, text cursors and selections, mouse pointers,
selected cells and ranges, running queries, the database itself, the open
sheet, the current lesson, the language and the semicolon mode.

The Lessons page is shared too: the same room link works on both pages, and
links (**Solve**, **Trainer**, **Lessons**, **All lessons**) take everyone in the
room along. On `/lessons` scrolling, the chosen lesson, the language and mouse
pointers are shared.

1. Start the server so other computers on your network can reach it:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8001
   ```
2. Open the page using your computer's network address, not `127.0.0.1`
   (find it with `ipconfig getifaddr en0` on macOS), e.g. `http://192.168.1.20:8001/`.
3. The address bar gets a `?room=…` part. Click **Copy invite link** and send it.
   Everyone with the same link is in the same room.

A room has one database, and each participant has their own connection to it. A
query runs once, on the connection of whoever pressed **Run**; everyone sees its
result and the new tables. An open transaction belongs to the person who began it:
others do not see its changes and wait on its locks, as in real PostgreSQL.

- Joining or reloading keeps the room's data. Closing a tab ends that person's
  connection and rolls back their open transaction; the database stays.
- Opening another lesson, **Reset** and switching the language put the seed data
  back for the whole room and end everyone's open transactions.
- Each student's progress and typed queries are kept in their own browser, so
  replacing the room's data loses nothing. A solved task counts for everyone in the room.
- A database with nobody connected is removed after 24 hours, or sooner when there
  are more than 30.

The room's live state (editor text, cursors, the log of shared actions) is kept in
the server's memory and disappears when the last person leaves or the server
restarts. The database stays on PostgreSQL.

## Deploy to Render

The repository is ready for [Render](https://render.com): `render.yaml` describes
the service, `requirements.txt` lists the dependencies and `.python-version`
pins Python 3.11.

1. Push the project to GitHub (or GitLab / Bitbucket).
2. In the Render dashboard choose **New → Blueprint** and pick the repository.
   Render reads `render.yaml`, creates the `sql-sheet` web service and the free PostgreSQL 18 database
   `sql-sheet-db`, connects them, and asks for `TEACHER_PASSWORD`.
3. Wait for the first deploy, then open `https://<name>.onrender.com` and open a lesson.

Without the Blueprint, create a **Web Service** by hand with:

| Setting | Value |
|---|---|
| Language | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| Health Check Path | `/healthz` |
| Environment | `DATABASE_ADMIN_URL` (the database's internal URL), `TEACHER_PASSWORD`, `SECRET_KEY` |

Notes:
- Keep **one instance**. Collaboration rooms live in the server's memory, so two
  instances would split people into different rooms.
- On the **free plan** the service sleeps after 15 minutes without traffic and
  the next visit takes about a minute to wake it. A restart clears all rooms and the page
  reconnects by itself. A room's database stays on PostgreSQL, but open transactions are lost.
- Render's free PostgreSQL **expires 30 days after creation**, and is deleted 14 days later. Students lose
  nothing, because progress is kept in the browser. To renew it, delete `sql-sheet-db` in the dashboard
  (a workspace can have only one free database), then sync the Blueprint to create it again.
- The database's account must be able to create roles and databases. If lessons say "Could not reach the
  database server", the service's log names the real error.

---

## Русский

Тренажёр SQL: запросы выполняются на настоящем сервере PostgreSQL,
а результат показывается как лист Excel — буквы столбцов, номера строк, строка формул,
сумма/среднее по выделению, подсветка добавленных и изменённых строк.

Интерфейс, уроки и учебная база есть на английском (по умолчанию) и русском.
Язык переключается кнопками EN / RU справа вверху и запоминается.
При смене языка учебная база загружается заново на выбранном языке.

### Запуск

```bash
make db     # PostgreSQL 18 в Docker
make run
```

Открой http://127.0.0.1:8001/. Адрес PostgreSQL задаёт `DATABASE_ADMIN_URL`; `Makefile` указывает
на локальный контейнер. Этой учётной записи нужны права создавать роли и базы. У каждой комнаты
одна база, ею владеет роль с минимальными правами `sheet_student`. Запрос останавливается через 20 секунд.

### Совместная работа

Несколько человек работают на одной странице в реальном времени. Общее всё:
текст запроса по мере набора, курсоры и выделения в редакторе, указатели мыши,
выделенные клетки и диапазоны, запуск запросов, сама база данных, открытый лист,
текущий урок, язык и режим точки с запятой.

Страница уроков тоже общая: одна ссылка на комнату работает на обеих страницах,
а переходы («Решить», «Тренажёр», «Уроки», «Все уроки») уводят за собой всех
участников. На `/lessons` общие прокрутка, выбранный урок, язык и курсоры мыши.

1. Запусти сервер так, чтобы к нему могли подключиться другие компьютеры в сети:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8001
   ```
2. Открой страницу по сетевому адресу компьютера, а не `127.0.0.1`
   (на macOS: `ipconfig getifaddr en0`), например `http://192.168.1.20:8001/`.
3. В адресе появится `?room=…`. Нажми **Скопировать ссылку** и отправь её.
   Все, кто открыл одну ссылку, работают в одной комнате.

У комнаты одна база, и у каждого участника своё соединение с ней. Запрос выполняется
один раз, в соединении того, кто нажал **Выполнить**; все видят его результат и новые таблицы.
Открытая транзакция принадлежит тому, кто её начал: другие не видят её изменений и ждут
её блокировок, как в настоящем PostgreSQL.

- Вход и перезагрузка страницы сохраняют данные комнаты. Закрытие вкладки завершает
  соединение этого человека и откатывает его открытую транзакцию; база остаётся.
- Переход на другой урок, **сброс** и смена языка возвращают исходные данные всей комнате
  и завершают открытые транзакции всех участников.
- Прогресс и набранные запросы каждого ученика хранятся в его браузере, поэтому замена
  данных комнаты ничего не стирает. Решённая задача засчитывается всем в комнате.
- База, к которой никто не подключён, удаляется через 24 часа, а если баз больше 30, то раньше.

Текущее состояние комнаты (текст редактора, курсоры, журнал общих действий) хранится в памяти
сервера и пропадает, когда все вышли или сервер перезапустился. База остаётся в PostgreSQL.

### Развёртывание на Render

1. Залей проект на GitHub.
2. В Render: **New → Blueprint**, выбери репозиторий. Render прочитает `render.yaml`, создаст сервис
   и бесплатную базу PostgreSQL 18 `sql-sheet-db`, свяжет их и спросит `TEACHER_PASSWORD`.
3. После первого деплоя открой `https://<имя>.onrender.com` и зайди в урок.

Держи **один экземпляр** сервиса: комнаты хранятся в памяти. На бесплатном плане
сервис засыпает через 15 минут без посетителей и просыпается примерно за минуту;
при перезапуске комнаты очищаются. База комнаты остаётся в PostgreSQL, но открытые транзакции теряются.
Бесплатная база Render **истекает через 30 дней** после создания, а ещё через 14 дней удаляется. Студенты
ничего не теряют: прогресс хранится в браузере. Чтобы продлить, удали `sql-sheet-db` в панели (бесплатная
база на рабочее пространство только одна) и синхронизируй Blueprint: он создаст базу заново.
Роль базы должна уметь создавать роли и базы. Если уроки пишут «Could not reach the database server»,
настоящая ошибка есть в логе сервиса.

### Уроки

`/lessons` — страница курса: план из 13 тем, а для готовых уроков теория, таблицы,
задания и ответы для преподавателя. Кнопка **Решить** открывает тренажёр с базой урока
(`/?lesson=1&task=3`), и после **Выполнить** результат сверяется с эталонным ответом.
Весь контент курса — в `course.py`: чтобы добавить урок, заполни `theory`,
`seed`, `tables`, `tasks` (у каждого задания нужен `answer`) и поставь `available: true`.

**После любого изменения данных, ответов, примеров или условий урока:**

1. Запусти `make results`. Команда прогонит весь SQL курса на PostgreSQL и перезапишет
   `course_results.json`. Если запрос падает, она назовёт задание и не запишет файл.
2. Закоммить `course_results.json` вместе с `course.py`. Сервер сверяет результаты учеников
   с этим файлом, и без него они будут проверяться по старым ответам.

Если забыть, `make check` упадёт с сообщением «run `make results`», а с ним и `make deploy`,
потому что он сначала запускает проверку. Для правки только текстов это не нужно.

### Преподаватель

Ответы видит только преподаватель: внизу урока на `/lessons` войди под логином
**teacher**. Пароль задаётся переменной окружения `TEACHER_PASSWORD`, по умолчанию
`sql2026`. На Render задай свой пароль: **Environment → Add variable**. Ответы
не попадают в браузер ученика: тренажёр отправляет результат на `/api/check`,
и сервер сам сравнивает его с ответом.

### Команды

Все команды в `Makefile`, список — `make`. Основные: `make install` (окружение и зависимости),
`make run` (запуск на порту 8001), `make run-lan` (запуск для других компьютеров в сети),
`make db` (PostgreSQL в Docker), `make results` (после изменения урока: прогнать его SQL на PostgreSQL и сохранить эталоны в `course_results.json`), `make check` (проверка кода, уроков и актуальности эталонов), `make deploy` (проверка, затем push
на GitHub, откуда Render развернёт новую версию).
