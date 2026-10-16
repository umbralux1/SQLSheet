# SQL Sheet

**English** · [Русский](#русский)

An SQL trainer that runs a real SQLite database in the browser (sql.js) and shows
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
| `make run` | Start locally with auto-reload on http://127.0.0.1:8001 (`PORT=8002 make run` for another port) |
| `make run-lan` | Start for other computers on your network and print the address to share |
| `make start` | Start like Render does, without reload |
| `make open` | Open the trainer and the lessons page in the browser |
| `make check` | Check the code, that every lesson answer and example runs, and that answers stay hidden |
| `make deploy` | Run the checks, refuse if something is not committed, then push to GitHub; Render deploys from there |
| `make deploy-hook` | Ask Render to redeploy right away (`RENDER_DEPLOY_HOOK=<url> make deploy-hook`) |
| `make status` | Show uncommitted files and commits not pushed yet |
| `make clean` | Remove Python caches |

## Run

```bash
source venv/bin/activate
uvicorn main:app --reload            # http://127.0.0.1:8000/
uvicorn main:app --reload --port 8001  # if port 8000 is taken
```

You can also open `static/index.html` directly in a browser.
An internet connection is required: the SQLite engine and fonts load from a CDN.

## Structure

- `main.py` — FastAPI app, serves the page at `/`
- `static/index.html` — the whole trainer (HTML + CSS + JS)
- Translations (`T`), sample data (`SEED`) and lessons (`LESSONS`) are at the top of the `<script>` in `index.html`

## Lessons

`/lessons` is the course page: a roadmap of 13 topics, and for each ready lesson
the theory, its tables, tasks and answers for teachers. **Solve** opens the trainer
with that lesson's database (`/?lesson=1&task=3`); after **Run** the result is
checked against the reference answer. Progress is saved in the browser.

All course content lives in `static/course.js`. To add a lesson, fill in its
`theory`, `seed`, `tables` and `tasks` (each task needs an `answer` query) and set
`available: true`.

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

The server keeps a log of every shared action and sends actions to everyone in
the same order, so all participants end up with identical databases; someone who
joins later replays the log. Rooms are kept in the server's memory and disappear
when the last person leaves or the server restarts. Collaboration needs the server;
opening `static/index.html` directly works in single-user mode.

## Deploy to Render

The repository is ready for [Render](https://render.com): `render.yaml` describes
the service, `requirements.txt` lists the dependencies and `.python-version`
pins Python 3.11.

1. Push the project to GitHub (or GitLab / Bitbucket).
2. In the Render dashboard choose **New → Blueprint** and pick the repository.
   Render reads `render.yaml` and creates the `sql-sheet` web service.
3. Wait for the first deploy, then open `https://<name>.onrender.com`.

Without the Blueprint, create a **Web Service** by hand with:

| Setting | Value |
|---|---|
| Language | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| Health Check Path | `/healthz` |

Notes:
- Keep **one instance**. Collaboration rooms live in the server's memory, so two
  instances would split people into different rooms.
- On the **free plan** the service sleeps after 15 minutes without traffic and
  the next visit takes a few seconds to wake it. A restart clears all rooms;
  the database in each browser is unaffected and the page reconnects by itself.

---

## Русский

Тренажёр SQL: запросы выполняются в настоящей SQLite прямо в браузере (sql.js),
а результат показывается как лист Excel — буквы столбцов, номера строк, строка формул,
сумма/среднее по выделению, подсветка добавленных и изменённых строк.

Интерфейс, уроки и учебная база есть на английском (по умолчанию) и русском.
Язык переключается кнопками EN / RU справа вверху и запоминается.
При смене языка учебная база загружается заново на выбранном языке.

### Запуск

```bash
source venv/bin/activate
uvicorn main:app --reload --port 8001
```

Открой http://127.0.0.1:8001/ — или просто открой `static/index.html` в браузере.

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

Сервер ведёт журнал общих действий и раздаёт их всем в одном порядке, поэтому
базы у всех участников одинаковые; кто подключился позже, проигрывает журнал.
Комнаты хранятся в памяти сервера и пропадают, когда все вышли или сервер
перезапустился.

### Развёртывание на Render

1. Залей проект на GitHub.
2. В Render: **New → Blueprint**, выбери репозиторий. Render прочитает `render.yaml`
   и сам создаст сервис.
3. После первого деплоя открой `https://<имя>.onrender.com`.

Держи **один экземпляр** сервиса: комнаты хранятся в памяти. На бесплатном плане
сервис засыпает через 15 минут без посетителей и просыпается за несколько секунд;
при перезапуске комнаты очищаются.

### Уроки

`/lessons` — страница курса: план из 13 тем, а для готовых уроков теория, таблицы,
задания и ответы для преподавателя. Кнопка **Решить** открывает тренажёр с базой урока
(`/?lesson=1&task=3`), и после **Выполнить** результат сверяется с эталонным ответом.
Весь контент курса — в `static/course.js`: чтобы добавить урок, заполни `theory`,
`seed`, `tables`, `tasks` (у каждого задания нужен `answer`) и поставь `available: true`.

### Преподаватель

Ответы видит только преподаватель: внизу урока на `/lessons` войди под логином
**teacher**. Пароль задаётся переменной окружения `TEACHER_PASSWORD`, по умолчанию
`sql2026`. На Render задай свой пароль: **Environment → Add variable**. Ответы
не попадают в браузер ученика: тренажёр отправляет результат на `/api/check`,
и сервер сам сравнивает его с ответом.

### Команды

Все команды в `Makefile`, список — `make`. Основные: `make install` (окружение и зависимости),
`make run` (запуск на порту 8001), `make run-lan` (запуск для других компьютеров в сети),
`make check` (проверка кода и всех ответов уроков), `make deploy` (проверка, затем push
на GitHub, откуда Render развернёт новую версию).
