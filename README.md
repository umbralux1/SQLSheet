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
