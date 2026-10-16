"""
SQL course content.

Everything here is served to the browser by /course.js EXCEPT the task answers,
which stay on the server: /api/check compares a student's result with the
answer's result, and /api/answers/<id> shows them to the logged-in teacher.

To add a lesson: fill in theory / seed / tables / tasks (every task needs an
"answer" query) and set "available": True.
"""

COURSE = {
    "lessons": [
        {
            "id": 1,
            "available": True,
            "title": {"en": "Introduction to SQL & SELECT", "ru": "Введение в SQL и SELECT"},
            "topics": {"en": "What is SQL, RDBMS, SELECT, FROM, columns", "ru": "Что такое SQL, реляционные СУБД, SELECT, FROM, столбцы"},
            "theory": {
                "en": '''<p><b>SQL</b> (Structured Query Language) is the language for working with <b>relational databases</b>, where data is stored in tables.</p>
<p>A <b>table</b> has <b>rows</b> (records) and <b>columns</b> (fields). In this trainer a table looks like an Excel sheet: every row is a record, every column is a field.</p>
<p>The most basic query:</p>
<pre class="code">SELECT column1, column2
FROM table_name;</pre>
<ul>
  <li><code>SELECT *</code> returns <b>all columns</b>.</li>
  <li>SQL keywords are usually written in <b>UPPERCASE</b>. It is not required, but it is the convention.</li>
  <li>Every statement ends with a <b>semicolon</b> <code>;</code>.</li>
</ul>
''',
                "ru": '''<p><b>SQL</b> (Structured Query Language) — язык для работы с <b>реляционными базами данных</b>, где данные хранятся в таблицах.</p>
<p>У <b>таблицы</b> есть <b>строки</b> (записи) и <b>столбцы</b> (поля). В тренажёре таблица выглядит как лист Excel: каждая строка — запись, каждый столбец — поле.</p>
<p>Самый простой запрос:</p>
<pre class="code">SELECT column1, column2
FROM table_name;</pre>
<ul>
  <li><code>SELECT *</code> возвращает <b>все столбцы</b>.</li>
  <li>Ключевые слова SQL принято писать <b>ЗАГЛАВНЫМИ</b>. Это не обязательно, но так принято.</li>
  <li>Каждая команда заканчивается <b>точкой с запятой</b> <code>;</code>.</li>
</ul>
''',
            },
            "tables": ["students", "books"],
            "seed": '''CREATE TABLE students (
    student_id   INT PRIMARY KEY,
    first_name   VARCHAR(50),
    last_name    VARCHAR(50),
    age          INT,
    city         VARCHAR(50),
    grade        INT
);
INSERT INTO students VALUES
(1, 'Alice',   'Brown',   16, 'London',   9),
(2, 'Bob',     'Smith',   15, 'Paris',    8),
(3, 'Charlie', 'Johnson', 17, 'London',  10),
(4, 'Diana',   'Miller',  16, 'Berlin',   9),
(5, 'Ethan',   'Davis',   14, 'Paris',    7),
(6, 'Fiona',   'Wilson',  17, 'Madrid',  10),
(7, 'George',  'Moore',   15, 'Berlin',   8),
(8, 'Hannah',  'Taylor',  16, 'London',   9);
CREATE TABLE books (
    book_id        INT PRIMARY KEY,
    title          VARCHAR(100),
    author         VARCHAR(50),
    year_published INT,
    price          DECIMAL(6,2),
    genre          VARCHAR(30)
);
INSERT INTO books VALUES
(1, 'The Silent River',   'J. K. Rowling',  1997, 12.50, 'Fantasy'),
(2, 'Beyond the Stars',   'I. Asimov',      1950,  9.99, 'Sci-Fi'),
(3, 'The Last Kingdom',   'B. Cornwell',    2004, 15.00, 'Historical'),
(4, 'Whispers of Time',   'A. Clarke',      1968, 11.75, 'Sci-Fi'),
(5, 'The Hidden Path',    'J. K. Rowling',  1998, 13.00, 'Fantasy'),
(6, 'Mountains of Ice',   'G. Martin',      1996, 20.00, 'Fantasy'),
(7, 'City of Ashes',      'A. Clarke',      1970, 10.25, 'Sci-Fi'),
(8, 'The Final Hour',     'B. Cornwell',    2007, 18.50, 'Historical');
''',
            "tasks": [
                {
                    "text": {"en": "Select all columns from the <code>students</code> table.", "ru": "Выбери все столбцы из таблицы <code>students</code>."},
                    "answer": "SELECT * FROM students;",
                },
                {
                    "text": {"en": "Select only <code>first_name</code> and <code>last_name</code> from <code>students</code>.", "ru": "Выбери только <code>first_name</code> и <code>last_name</code> из <code>students</code>."},
                    "answer": "SELECT first_name, last_name FROM students;",
                },
                {
                    "text": {"en": "Select <code>title</code> and <code>price</code> from <code>books</code>.", "ru": "Выбери <code>title</code> и <code>price</code> из <code>books</code>."},
                    "answer": "SELECT title, price FROM books;",
                },
                {
                    "text": {"en": "Select all columns from <code>books</code>.", "ru": "Выбери все столбцы из <code>books</code>."},
                    "answer": "SELECT * FROM books;",
                },
                {
                    "text": {"en": "Select <code>first_name</code>, <code>city</code> and <code>grade</code> from <code>students</code>.", "ru": "Выбери <code>first_name</code>, <code>city</code> и <code>grade</code> из <code>students</code>."},
                    "answer": "SELECT first_name, city, grade FROM students;",
                },
                {
                    "text": {"en": "Select only the <code>author</code> column from <code>books</code>.", "ru": "Выбери только столбец <code>author</code> из <code>books</code>."},
                    "answer": "SELECT author FROM books;",
                },
                {
                    "text": {"en": "Select <code>title</code>, <code>year_published</code> and <code>genre</code> from <code>books</code>.", "ru": "Выбери <code>title</code>, <code>year_published</code> и <code>genre</code> из <code>books</code>."},
                    "answer": "SELECT title, year_published, genre FROM books;",
                },
                {
                    "text": {"en": "Select <code>student_id</code> and <code>age</code> from <code>students</code>.", "ru": "Выбери <code>student_id</code> и <code>age</code> из <code>students</code>."},
                    "answer": "SELECT student_id, age FROM students;",
                },
                {
                    "text": {"en": "Select only <code>book_id</code>, <code>title</code> and <code>author</code> from <code>books</code>.", "ru": "Выбери только <code>book_id</code>, <code>title</code> и <code>author</code> из <code>books</code>."},
                    "answer": "SELECT book_id, title, author FROM books;",
                },
                {
                    "text": {"en": "Select <code>city</code> and <code>grade</code> from <code>students</code>.", "ru": "Выбери <code>city</code> и <code>grade</code> из <code>students</code>."},
                    "answer": "SELECT city, grade FROM students;",
                },
            ],
        },
        {
            "id": 2,
            "available": False,
            "title": {"en": "WHERE & Filtering", "ru": "WHERE и фильтрация"},
            "topics": {"en": "Comparison operators, AND/OR/NOT, BETWEEN, IN, LIKE, NULL", "ru": "Операторы сравнения, AND/OR/NOT, BETWEEN, IN, LIKE, NULL"},
        },
        {
            "id": 3,
            "available": False,
            "title": {"en": "ORDER BY & LIMIT", "ru": "ORDER BY и LIMIT"},
            "topics": {"en": "Sorting, top-N queries", "ru": "Сортировка, первые N строк"},
        },
        {
            "id": 4,
            "available": False,
            "title": {"en": "Aggregate Functions", "ru": "Агрегатные функции"},
            "topics": {"en": "COUNT, SUM, AVG, MIN, MAX", "ru": "COUNT, SUM, AVG, MIN, MAX"},
        },
        {
            "id": 5,
            "available": False,
            "title": {"en": "GROUP BY & HAVING", "ru": "GROUP BY и HAVING"},
            "topics": {"en": "Grouping data, filtering groups", "ru": "Группировка данных, фильтрация групп"},
        },
        {
            "id": 6,
            "available": False,
            "title": {"en": "JOINs", "ru": "JOIN"},
            "topics": {"en": "INNER, LEFT, RIGHT, FULL, SELF JOIN", "ru": "INNER, LEFT, RIGHT, FULL, SELF JOIN"},
        },
        {
            "id": 7,
            "available": False,
            "title": {"en": "Subqueries", "ru": "Подзапросы"},
            "topics": {"en": "Scalar, IN, EXISTS, correlated", "ru": "Скалярные, IN, EXISTS, коррелированные"},
        },
        {
            "id": 8,
            "available": False,
            "title": {"en": "Set Operations", "ru": "Операции над множествами"},
            "topics": {"en": "UNION, INTERSECT, EXCEPT", "ru": "UNION, INTERSECT, EXCEPT"},
        },
        {
            "id": 9,
            "available": False,
            "title": {"en": "CASE, COALESCE, NULL handling", "ru": "CASE, COALESCE и работа с NULL"},
            "topics": {"en": "Conditional logic in SQL", "ru": "Условная логика в SQL"},
        },
        {
            "id": 10,
            "available": False,
            "title": {"en": "Window Functions", "ru": "Оконные функции"},
            "topics": {"en": "ROW_NUMBER, RANK, LAG, LEAD, OVER", "ru": "ROW_NUMBER, RANK, LAG, LEAD, OVER"},
        },
        {
            "id": 11,
            "available": False,
            "title": {"en": "CTEs", "ru": "CTE"},
            "topics": {"en": "WITH clause, recursive CTEs", "ru": "Конструкция WITH, рекурсивные CTE"},
        },
        {
            "id": 12,
            "available": False,
            "title": {"en": "DDL & DML", "ru": "DDL и DML"},
            "topics": {"en": "CREATE, INSERT, UPDATE, DELETE, ALTER", "ru": "CREATE, INSERT, UPDATE, DELETE, ALTER"},
        },
        {
            "id": 13,
            "available": False,
            "title": {"en": "Indexes, Views, Transactions", "ru": "Индексы, представления, транзакции"},
            "topics": {"en": "Performance & data integrity basics", "ru": "Основы производительности и целостности данных"},
        },
    ]
}
