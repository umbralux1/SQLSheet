# SQL Sheet

**English** · [Русский](#русский)

An SQL trainer that runs a real SQLite database in the browser (sql.js) and shows
query results as a spreadsheet: column letters, row numbers, a formula bar,
sum/average/count for the selection, and highlighting of inserted and updated rows.

The interface, lessons and sample database are available in English (default) and
Russian. Switch with the EN / RU buttons in the top right; the choice is remembered.
Switching the language reloads the sample database in that language.

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

## Working together

Two or more people work on the same page in real time. Everything is shared:
the query text as it is typed, text cursors and selections, mouse pointers,
selected cells and ranges, running queries, the database itself, the open
sheet, the current lesson, the language and the semicolon mode.

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
