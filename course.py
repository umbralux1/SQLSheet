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
            "available": True,
            "title": {"en": "WHERE & Filtering", "ru": "WHERE и фильтрация"},
            "topics": {"en": "Comparison operators, AND/OR/NOT, BETWEEN, IN, LIKE, NULL", "ru": "Операторы сравнения, AND/OR/NOT, BETWEEN, IN, LIKE, NULL"},
            "theory": {
                "en": '''<p>The <code>WHERE</code> clause filters rows <b>before</b> they are returned. In Excel terms it is the filter on a column.</p>
<pre class="code">SELECT column1, column2
FROM table_name
WHERE condition;</pre>
<h4>Comparison operators</h4>
<table class="ops"><thead><tr><th>Operator</th><th>Meaning</th></tr></thead><tbody>
<tr><td><code>=</code></td><td>equal</td></tr>
<tr><td><code>&lt;&gt;</code> or <code>!=</code></td><td>not equal</td></tr>
<tr><td><code>&gt;</code></td><td>greater than</td></tr>
<tr><td><code>&lt;</code></td><td>less than</td></tr>
<tr><td><code>&gt;=</code></td><td>greater or equal</td></tr>
<tr><td><code>&lt;=</code></td><td>less or equal</td></tr>
</tbody></table>
<h4>Logical operators</h4>
<ul>
  <li><code>AND</code> — both conditions must be true</li>
  <li><code>OR</code> — at least one condition is true</li>
  <li><code>NOT</code> — reverses a condition</li>
  <li>Use <b>parentheses</b> to group conditions: <code>WHERE (a OR b) AND c</code></li>
</ul>
<h4>Special operators</h4>
<ul>
  <li><code>BETWEEN x AND y</code> — inclusive range</li>
  <li><code>IN (v1, v2, ...)</code> — matches any value in a list</li>
  <li><code>LIKE</code> — pattern matching: <code>%</code> is any number of characters, <code>_</code> is exactly one character</li>
  <li><code>IS NULL</code> / <code>IS NOT NULL</code> — check for NULL (never use <code>= NULL</code>)</li>
</ul>
''',
                "ru": '''<p><code>WHERE</code> отбирает строки <b>до</b> того, как они попадут в результат. Если сравнивать с Excel, это фильтр по столбцу.</p>
<pre class="code">SELECT column1, column2
FROM table_name
WHERE condition;</pre>
<h4>Операторы сравнения</h4>
<table class="ops"><thead><tr><th>Оператор</th><th>Значение</th></tr></thead><tbody>
<tr><td><code>=</code></td><td>равно</td></tr>
<tr><td><code>&lt;&gt;</code> или <code>!=</code></td><td>не равно</td></tr>
<tr><td><code>&gt;</code></td><td>больше</td></tr>
<tr><td><code>&lt;</code></td><td>меньше</td></tr>
<tr><td><code>&gt;=</code></td><td>больше или равно</td></tr>
<tr><td><code>&lt;=</code></td><td>меньше или равно</td></tr>
</tbody></table>
<h4>Логические операторы</h4>
<ul>
  <li><code>AND</code> — оба условия должны быть верны</li>
  <li><code>OR</code> — верно хотя бы одно условие</li>
  <li><code>NOT</code> — меняет условие на противоположное</li>
  <li><b>Скобки</b> группируют условия: <code>WHERE (a OR b) AND c</code></li>
</ul>
<h4>Специальные операторы</h4>
<ul>
  <li><code>BETWEEN x AND y</code> — диапазон, включая границы</li>
  <li><code>IN (v1, v2, ...)</code> — совпадение с любым значением из списка</li>
  <li><code>LIKE</code> — поиск по шаблону: <code>%</code> — любое число символов, <code>_</code> — ровно один символ</li>
  <li><code>IS NULL</code> / <code>IS NOT NULL</code> — проверка на NULL (никогда не пиши <code>= NULL</code>)</li>
</ul>
''',
            },
            # Only the logged-in teacher sees these (served with the answers).
            "tips": {
                "en": [
                    "Watch for common mistakes: <code>= NULL</code> instead of <code>IS NULL</code>, and missing parentheses when mixing <code>AND</code> and <code>OR</code>.",
                    "Ask the student to <b>predict the row count</b> before running a query. It builds intuition.",
                    "Have them <b>modify</b> queries, for example change <code>&gt;</code> to <code>&gt;=</code>: what changes?",
                ],
                "ru": [
                    "Следи за типичными ошибками: <code>= NULL</code> вместо <code>IS NULL</code> и забытые скобки, когда смешиваются <code>AND</code> и <code>OR</code>.",
                    "Проси ученика <b>предсказать число строк</b> до запуска запроса. Это развивает интуицию.",
                    "Предлагай <b>менять</b> запросы, например заменить <code>&gt;</code> на <code>&gt;=</code>: что изменится?",
                ],
            },
            "tables": ["employees", "products"],
            "seed": '''CREATE TABLE employees (
    emp_id      INT PRIMARY KEY,
    first_name  VARCHAR(50),
    last_name   VARCHAR(50),
    department  VARCHAR(30),
    salary      INT,
    hire_year   INT,
    city        VARCHAR(50),
    bonus       INT
);
INSERT INTO employees VALUES
(1,  'Alice',   'Brown',   'IT',      60000, 2018, 'London',  5000),
(2,  'Bob',     'Smith',   'HR',      45000, 2019, 'Paris',   NULL),
(3,  'Charlie', 'Johnson', 'IT',      75000, 2015, 'London',  8000),
(4,  'Diana',   'Miller',  'Sales',   52000, 2020, 'Berlin',  3000),
(5,  'Ethan',   'Davis',   'IT',      68000, 2017, 'Paris',   NULL),
(6,  'Fiona',   'Wilson',  'Sales',   48000, 2021, 'Madrid',  2000),
(7,  'George',  'Moore',   'HR',      55000, 2016, 'Berlin',  4000),
(8,  'Hannah',  'Taylor',  'Sales',   62000, 2018, 'London',  6000),
(9,  'Ivan',    'Petrov',  'IT',      90000, 2014, 'Madrid',  10000),
(10, 'Julia',   'Adams',   'HR',      41000, 2022, 'Paris',   NULL);
CREATE TABLE products (
    product_id   INT PRIMARY KEY,
    product_name VARCHAR(50),
    category     VARCHAR(30),
    price        DECIMAL(7,2),
    stock        INT,
    supplier     VARCHAR(50)
);
INSERT INTO products VALUES
(1,  'Laptop Pro',      'Electronics', 1200.00, 15,  'TechCorp'),
(2,  'Wireless Mouse',  'Electronics',   25.50, 200, 'GadgetInc'),
(3,  'Office Chair',    'Furniture',    180.00, 40,  'ComfortPlus'),
(4,  'Notebook',        'Stationery',     3.20, 500, 'PaperWorld'),
(5,  'Monitor 27"',     'Electronics',  350.00, 30,  'TechCorp'),
(6,  'Desk Lamp',       'Furniture',     45.00, 80,  'BrightHome'),
(7,  'Pen Set',         'Stationery',     8.75, 300, 'PaperWorld'),
(8,  'Keyboard',        'Electronics',   75.00, 120, 'GadgetInc'),
(9,  'Bookshelf',       'Furniture',    220.00, 20,  'ComfortPlus'),
(10, 'Stapler',         'Stationery',    12.40, 150, 'PaperWorld');
''',
            "tasks": [
                # Section A
                {"section": {"en": "A · Comparison operators", "ru": "A · Операторы сравнения"},
                 "text": {"en": "Get all employees whose <code>salary</code> is greater than 60000.", "ru": "Выведи всех сотрудников, у которых <code>salary</code> больше 60000."},
                 "answer": "SELECT * FROM employees WHERE salary > 60000;"},
                {"text": {"en": "Get all employees who work in the <code>'IT'</code> department.", "ru": "Выведи всех сотрудников отдела <code>'IT'</code>."},
                 "answer": "SELECT * FROM employees WHERE department = 'IT';"},
                {"text": {"en": "Get all products whose <code>price</code> is less than 50.", "ru": "Выведи все товары с ценой (<code>price</code>) меньше 50."},
                 "answer": "SELECT * FROM products WHERE price < 50;"},
                {"text": {"en": "Get all employees hired in 2018.", "ru": "Выведи всех сотрудников, нанятых в 2018 году."},
                 "answer": "SELECT * FROM employees WHERE hire_year = 2018;"},
                {"text": {"en": "Get all products with <code>stock</code> equal to 0 (if any). Check with <code>=</code>.", "ru": "Выведи все товары, у которых <code>stock</code> равен 0 (если такие есть). Проверь через <code>=</code>."},
                 "answer": "SELECT * FROM products WHERE stock = 0;"},
                {"text": {"en": "Get all employees whose salary is not equal to 45000.", "ru": "Выведи всех сотрудников, у которых зарплата не равна 45000."},
                 "answer": "SELECT * FROM employees WHERE salary <> 45000;"},
                {"text": {"en": "Get all products with price greater than or equal to 200.", "ru": "Выведи все товары с ценой больше или равной 200."},
                 "answer": "SELECT * FROM products WHERE price >= 200;"},
                {"text": {"en": "Get all employees hired <b>before</b> 2017.", "ru": "Выведи всех сотрудников, нанятых <b>до</b> 2017 года."},
                 "answer": "SELECT * FROM employees WHERE hire_year < 2017;"},
                # Section B
                {"section": {"en": "B · AND / OR / NOT", "ru": "B · AND / OR / NOT"},
                 "text": {"en": "Get all IT employees with salary greater than 65000.", "ru": "Выведи всех сотрудников IT с зарплатой больше 65000."},
                 "answer": "SELECT * FROM employees WHERE department = 'IT' AND salary > 65000;"},
                {"text": {"en": "Get all employees from <code>'London'</code> OR <code>'Paris'</code>.", "ru": "Выведи всех сотрудников из <code>'London'</code> ИЛИ <code>'Paris'</code>."},
                 "answer": "SELECT * FROM employees WHERE city = 'London' OR city = 'Paris';"},
                {"text": {"en": "Get all employees from <code>'London'</code> or <code>'Paris'</code> <b>whose salary is above 50000</b>.", "ru": "Выведи всех сотрудников из <code>'London'</code> или <code>'Paris'</code> <b>с зарплатой выше 50000</b>."},
                 "answer": "SELECT * FROM employees\nWHERE (city = 'London' OR city = 'Paris') AND salary > 50000;"},
                {"text": {"en": "Get all products in the <code>'Electronics'</code> category with price below 500.", "ru": "Выведи все товары категории <code>'Electronics'</code> с ценой меньше 500."},
                 "answer": "SELECT * FROM products WHERE category = 'Electronics' AND price < 500;"},
                {"text": {"en": "Get all employees NOT in the <code>'HR'</code> department.", "ru": "Выведи всех сотрудников, которые НЕ работают в отделе <code>'HR'</code>."},
                 "answer": "SELECT * FROM employees WHERE NOT department = 'HR';"},
                {"text": {"en": "Get all products that are NOT in <code>'Stationery'</code> and cost more than 100.", "ru": "Выведи все товары НЕ из категории <code>'Stationery'</code> дороже 100."},
                 "answer": "SELECT * FROM products WHERE NOT category = 'Stationery' AND price > 100;"},
                # Section C
                {"section": {"en": "C · BETWEEN", "ru": "C · BETWEEN"},
                 "text": {"en": "Get all employees with salary between 45000 and 65000 (inclusive).", "ru": "Выведи всех сотрудников с зарплатой от 45000 до 65000 включительно."},
                 "answer": "SELECT * FROM employees WHERE salary BETWEEN 45000 AND 65000;"},
                {"text": {"en": "Get all products with price between 20 and 200.", "ru": "Выведи все товары с ценой от 20 до 200."},
                 "answer": "SELECT * FROM products WHERE price BETWEEN 20 AND 200;"},
                {"text": {"en": "Get all employees hired between 2016 and 2019.", "ru": "Выведи всех сотрудников, нанятых с 2016 по 2019 год."},
                 "answer": "SELECT * FROM employees WHERE hire_year BETWEEN 2016 AND 2019;"},
                {"text": {"en": "Get all products with stock between 50 and 200.", "ru": "Выведи все товары, у которых <code>stock</code> от 50 до 200."},
                 "answer": "SELECT * FROM products WHERE stock BETWEEN 50 AND 200;"},
                # Section D
                {"section": {"en": "D · IN", "ru": "D · IN"},
                 "text": {"en": "Get all employees who work in <code>'IT'</code> or <code>'Sales'</code> (use <code>IN</code>).", "ru": "Выведи всех сотрудников отделов <code>'IT'</code> и <code>'Sales'</code> (используй <code>IN</code>)."},
                 "answer": "SELECT * FROM employees WHERE department IN ('IT', 'Sales');"},
                {"text": {"en": "Get all products from suppliers <code>'TechCorp'</code> or <code>'PaperWorld'</code>.", "ru": "Выведи все товары поставщиков <code>'TechCorp'</code> и <code>'PaperWorld'</code>."},
                 "answer": "SELECT * FROM products WHERE supplier IN ('TechCorp', 'PaperWorld');"},
                {"text": {"en": "Get all employees from the cities <code>'London'</code>, <code>'Berlin'</code>, <code>'Madrid'</code>.", "ru": "Выведи всех сотрудников из городов <code>'London'</code>, <code>'Berlin'</code>, <code>'Madrid'</code>."},
                 "answer": "SELECT * FROM employees WHERE city IN ('London', 'Berlin', 'Madrid');"},
                {"text": {"en": "Get all products in the categories <code>'Electronics'</code> or <code>'Furniture'</code>.", "ru": "Выведи все товары категорий <code>'Electronics'</code> и <code>'Furniture'</code>."},
                 "answer": "SELECT * FROM products WHERE category IN ('Electronics', 'Furniture');"},
                # Section E
                {"section": {"en": "E · LIKE", "ru": "E · LIKE"},
                 "text": {"en": "Get all employees whose first name starts with <code>'A'</code>.", "ru": "Выведи всех сотрудников, чьё имя начинается на <code>'A'</code>."},
                 "answer": "SELECT * FROM employees WHERE first_name LIKE 'A%';"},
                {"text": {"en": "Get all products whose name ends with <code>'e'</code>.", "ru": "Выведи все товары, название которых заканчивается на <code>'e'</code>."},
                 "answer": "SELECT * FROM products WHERE product_name LIKE '%e';"},
                {"text": {"en": "Get all employees whose last name contains <code>'son'</code>.", "ru": "Выведи всех сотрудников, в фамилии которых есть <code>'son'</code>."},
                 "answer": "SELECT * FROM employees WHERE last_name LIKE '%son%';"},
                {"text": {"en": "Get all products whose name contains the word <code>'Set'</code>.", "ru": "Выведи все товары, в названии которых есть слово <code>'Set'</code>."},
                 "answer": "SELECT * FROM products WHERE product_name LIKE '%Set%';"},
                {"text": {"en": "Get all employees whose first name has exactly 5 letters (use <code>_</code>).", "ru": "Выведи всех сотрудников, чьё имя состоит ровно из 5 букв (используй <code>_</code>)."},
                 "answer": "SELECT * FROM employees WHERE first_name LIKE '_____';"},
                {"text": {"en": "Get all products whose name starts with <code>'B'</code>.", "ru": "Выведи все товары, название которых начинается на <code>'B'</code>."},
                 "answer": "SELECT * FROM products WHERE product_name LIKE 'B%';"},
                # Section F
                {"section": {"en": "F · NULL", "ru": "F · NULL"},
                 "text": {"en": "Get all employees who have a bonus (<code>bonus IS NOT NULL</code>).", "ru": "Выведи всех сотрудников, у которых есть бонус (<code>bonus IS NOT NULL</code>)."},
                 "answer": "SELECT * FROM employees WHERE bonus IS NOT NULL;"},
                {"text": {"en": "Get all employees who do NOT have a bonus.", "ru": "Выведи всех сотрудников, у которых НЕТ бонуса."},
                 "answer": "SELECT * FROM employees WHERE bonus IS NULL;"},
                {"text": {"en": "Get all employees who have a bonus greater than 4000.", "ru": "Выведи всех сотрудников с бонусом больше 4000."},
                 "answer": "SELECT * FROM employees WHERE bonus > 4000;"},
                # Section G
                {"section": {"en": "G · Mixed", "ru": "G · Всё вместе"},
                 "text": {"en": "Get all IT or Sales employees from <code>'London'</code> with salary &gt; 55000.", "ru": "Выведи всех сотрудников IT или Sales из <code>'London'</code> с зарплатой &gt; 55000."},
                 "answer": "SELECT * FROM employees\nWHERE department IN ('IT', 'Sales')\n  AND city = 'London'\n  AND salary > 55000;"},
                {"text": {"en": "Get all products in <code>'Electronics'</code> with price <code>BETWEEN</code> 50 <code>AND</code> 400 and stock &gt; 20.", "ru": "Выведи все товары <code>'Electronics'</code> с ценой <code>BETWEEN</code> 50 <code>AND</code> 400 и <code>stock</code> &gt; 20."},
                 "answer": "SELECT * FROM products\nWHERE category = 'Electronics'\n  AND price BETWEEN 50 AND 400\n  AND stock > 20;"},
                {"text": {"en": "Get all employees whose first name starts with <code>'J'</code> OR last name starts with <code>'B'</code>.", "ru": "Выведи всех сотрудников, у которых имя начинается на <code>'J'</code> ИЛИ фамилия на <code>'B'</code>."},
                 "answer": "SELECT * FROM employees\nWHERE first_name LIKE 'J%' OR last_name LIKE 'B%';"},
                {"text": {"en": "Get all products whose name contains <code>'o'</code> and whose category is NOT <code>'Furniture'</code>.", "ru": "Выведи все товары, в названии которых есть <code>'o'</code>, а категория НЕ <code>'Furniture'</code>."},
                 "answer": "SELECT * FROM products\nWHERE product_name LIKE '%o%' AND category <> 'Furniture';"},
            ],
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
