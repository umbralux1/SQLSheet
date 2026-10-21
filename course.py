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
                {"id": "1.1", 
                    "text": {"en": "Select all columns from the <code>students</code> table.", "ru": "Выбери все столбцы из таблицы <code>students</code>."},
                    "answer": "SELECT * FROM students;",
                },
                {"id": "1.2", 
                    "text": {"en": "Select only <code>first_name</code> and <code>last_name</code> from <code>students</code>.", "ru": "Выбери только <code>first_name</code> и <code>last_name</code> из <code>students</code>."},
                    "answer": "SELECT first_name, last_name FROM students;",
                },
                {"id": "1.3", 
                    "text": {"en": "Select <code>title</code> and <code>price</code> from <code>books</code>.", "ru": "Выбери <code>title</code> и <code>price</code> из <code>books</code>."},
                    "answer": "SELECT title, price FROM books;",
                },
                {"id": "1.4", 
                    "text": {"en": "Select all columns from <code>books</code>.", "ru": "Выбери все столбцы из <code>books</code>."},
                    "answer": "SELECT * FROM books;",
                },
                {"id": "1.5", 
                    "text": {"en": "Select <code>first_name</code>, <code>city</code> and <code>grade</code> from <code>students</code>.", "ru": "Выбери <code>first_name</code>, <code>city</code> и <code>grade</code> из <code>students</code>."},
                    "answer": "SELECT first_name, city, grade FROM students;",
                },
                {"id": "1.6", 
                    "text": {"en": "Select only the <code>author</code> column from <code>books</code>.", "ru": "Выбери только столбец <code>author</code> из <code>books</code>."},
                    "answer": "SELECT author FROM books;",
                },
                {"id": "1.7", 
                    "text": {"en": "Select <code>title</code>, <code>year_published</code> and <code>genre</code> from <code>books</code>.", "ru": "Выбери <code>title</code>, <code>year_published</code> и <code>genre</code> из <code>books</code>."},
                    "answer": "SELECT title, year_published, genre FROM books;",
                },
                {"id": "1.8", 
                    "text": {"en": "Select <code>student_id</code> and <code>age</code> from <code>students</code>.", "ru": "Выбери <code>student_id</code> и <code>age</code> из <code>students</code>."},
                    "answer": "SELECT student_id, age FROM students;",
                },
                {"id": "1.9", 
                    "text": {"en": "Select only <code>book_id</code>, <code>title</code> and <code>author</code> from <code>books</code>.", "ru": "Выбери только <code>book_id</code>, <code>title</code> и <code>author</code> из <code>books</code>."},
                    "answer": "SELECT book_id, title, author FROM books;",
                },
                {"id": "1.10", 
                    "text": {"en": "Select <code>city</code> and <code>grade</code> from <code>students</code>.", "ru": "Выбери <code>city</code> и <code>grade</code> из <code>students</code>."},
                    "answer": "SELECT city, grade FROM students;",
                },
            ],
        },
        {
            "id": 2,
            "available": True,
            "title": {"en": "WHERE & Filtering", "ru": "WHERE и фильтрация"},
            "topics": {"en": "Comparison operators, AND/OR/NOT, BETWEEN, IN, LIKE, NULL, DISTINCT", "ru": "Операторы сравнения, AND/OR/NOT, BETWEEN, IN, LIKE, NULL, DISTINCT"},
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
<h4>Removing duplicates</h4>
<ul>
  <li><code>SELECT DISTINCT column</code> — returns each value only once</li>
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
<h4>Удаление повторов</h4>
<ul>
  <li><code>SELECT DISTINCT column</code> — возвращает каждое значение один раз</li>
</ul>
''',
            },
            # Only the logged-in teacher sees these (served with the answers).
            "tips": {
                "en": [
                    "Watch for common mistakes: <code>= NULL</code> instead of <code>IS NULL</code>, and missing parentheses when mixing <code>AND</code> and <code>OR</code>.",
                    "Ask the student to <b>predict the row count</b> before running a query. It builds intuition.",
                    "Have them <b>modify</b> queries, for example change <code>&gt;</code> to <code>&gt;=</code>: what changes?",
                    "<b>B+++</b> and <b>B++++</b>: the first 12 tasks are predictions. The student answers Yes/No about one person, or marks everyone who will pass, and only then sees the real result and an explanation. Ask her to explain her answer out loud before pressing the button. In the De Morgan tasks, the most common mistake is forgetting to swap <code>AND</code> and <code>OR</code>: the trainer catches it.",
                    "<b>B++</b> (brackets with <code>AND</code> + <code>OR</code>) was added after <code>city = 'Paris' OR 'Berlin' AND salary &gt; 50000</code>. In every task the version without brackets returns different rows, so the trainer catches it. Ask the student to run the wrong version first and say who should not be in the result.",
                    "If task 10 is hard, use section <b>B+</b>: ten more <code>OR</code> tasks. Show both wrong versions from its theory and ask the student to predict their row counts first.",
                    "<b>Extra practice</b> (50 tasks) repeats the lesson's topics and is optional. Good for homework or for a student who finished early.",
                    "<b>Extra AND / OR / NOT</b> introduces De Morgan's law: <code>NOT (A OR B)</code> equals <code>NOT A AND NOT B</code>. Ask the student to write each task both ways and compare the row counts.",
                    "<b>Extra LIKE</b>: <code>_</code> is exactly one character and <code>%</code> is any number. In this trainer (SQLite) <code>LIKE</code> ignores letter case, so <code>'%i%'</code> also finds Ivan. Other databases may differ.",
                    "<b>Extra NULL</b>, the last task: <code>bonus &lt; 4000</code> alone skips the employees with no bonus, because a comparison with NULL is never true. That is why <code>bonus IS NULL OR …</code> is needed.",
                ],
                "ru": [
                    "Следи за типичными ошибками: <code>= NULL</code> вместо <code>IS NULL</code> и забытые скобки, когда смешиваются <code>AND</code> и <code>OR</code>.",
                    "Проси ученика <b>предсказать число строк</b> до запуска запроса. Это развивает интуицию.",
                    "Предлагай <b>менять</b> запросы, например заменить <code>&gt;</code> на <code>&gt;=</code>: что изменится?",
                    "<b>B+++</b> и <b>B++++</b>: первые 12 заданий — на предсказание. Ученик отвечает «да / нет» про одного человека или отмечает всех, кто попадёт в результат, и только потом видит настоящий результат и объяснение. Проси объяснить ответ вслух до нажатия кнопки. В заданиях на де Моргана самая частая ошибка — забыть поменять <code>AND</code> и <code>OR</code>: тренажёр её поймает.",
                    "<b>B++</b> (скобки при <code>AND</code> + <code>OR</code>) добавлен после запроса <code>city = 'Paris' OR 'Berlin' AND salary &gt; 50000</code>. В каждом задании вариант без скобок возвращает другие строки, и тренажёр его не засчитает. Попроси ученика сначала запустить неверный вариант и сказать, кого в результате быть не должно.",
                    "Если задание 10 даётся тяжело, переходи к разделу <b>B+</b>: ещё десять заданий на <code>OR</code>. Покажи обе ошибки из его теории и попроси сначала предсказать, сколько строк они вернут.",
                    "<b>Дополнительная практика</b> (50 заданий) повторяет темы урока и не обязательна. Подходит для домашней работы или для ученика, который закончил раньше.",
                    "<b>Доп. AND / OR / NOT</b> знакомит с законом де Моргана: <code>NOT (A OR B)</code> равно <code>NOT A AND NOT B</code>. Попроси записать каждое задание обоими способами и сравнить число строк.",
                    "<b>Доп. LIKE</b>: <code>_</code> — ровно один символ, <code>%</code> — любое количество. В этом тренажёре (SQLite) <code>LIKE</code> не различает регистр, поэтому <code>'%i%'</code> находит и Ivan. В других СУБД может быть иначе.",
                    "<b>Доп. NULL</b>, последнее задание: одно условие <code>bonus &lt; 4000</code> пропустит сотрудников без бонуса, потому что сравнение с NULL никогда не верно. Поэтому нужно <code>bonus IS NULL OR …</code>.",
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
                {"id": "2.1", "section": {"en": "A · Comparison operators", "ru": "A · Операторы сравнения"},
                 "intro": {
                     "en": '''<p><code>WHERE</code> keeps only the rows where the condition is true. A condition compares a column with a value using <code>=</code>, <code>&lt;&gt;</code>, <code>&gt;</code>, <code>&lt;</code>, <code>&gt;=</code>, <code>&lt;=</code>. Text goes in single quotes (<code>'Berlin'</code>), numbers go without quotes (<code>60000</code>).</p>
<p><b>Example:</b> employees who work in Berlin.</p>''',
                     "ru": '''<p><code>WHERE</code> оставляет только строки, для которых условие верно. Условие сравнивает столбец со значением: <code>=</code>, <code>&lt;&gt;</code>, <code>&gt;</code>, <code>&lt;</code>, <code>&gt;=</code>, <code>&lt;=</code>. Текст пишется в одинарных кавычках (<code>'Berlin'</code>), числа без кавычек (<code>60000</code>).</p>
<p><b>Пример:</b> сотрудники, которые работают в Берлине.</p>''',
                 },
                 "example": "SELECT first_name, city\nFROM employees\nWHERE city = 'Berlin';",
                 "text": {"en": "Get all employees whose <code>salary</code> is greater than 60000.", "ru": "Выведи всех сотрудников, у которых <code>salary</code> больше 60000."},
                 "answer": "SELECT * FROM employees WHERE salary > 60000;"},
                {"id": "2.2", "text": {"en": "Get all employees who work in the <code>'IT'</code> department.", "ru": "Выведи всех сотрудников отдела <code>'IT'</code>."},
                 "answer": "SELECT * FROM employees WHERE department = 'IT';"},
                {"id": "2.3", "text": {"en": "Get all products whose <code>price</code> is less than 50.", "ru": "Выведи все товары с ценой (<code>price</code>) меньше 50."},
                 "answer": "SELECT * FROM products WHERE price < 50;"},
                {"id": "2.4", "text": {"en": "Get all employees hired in 2018.", "ru": "Выведи всех сотрудников, нанятых в 2018 году."},
                 "answer": "SELECT * FROM employees WHERE hire_year = 2018;"},
                {"id": "2.5", "text": {"en": "Get all products with <code>stock</code> equal to 0 (if any). Check with <code>=</code>.", "ru": "Выведи все товары, у которых <code>stock</code> равен 0 (если такие есть). Проверь через <code>=</code>."},
                 "answer": "SELECT * FROM products WHERE stock = 0;"},
                {"id": "2.6", "text": {"en": "Get all employees whose salary is not equal to 45000.", "ru": "Выведи всех сотрудников, у которых зарплата не равна 45000."},
                 "answer": "SELECT * FROM employees WHERE salary <> 45000;"},
                {"id": "2.7", "text": {"en": "Get all products with price greater than or equal to 200.", "ru": "Выведи все товары с ценой больше или равной 200."},
                 "answer": "SELECT * FROM products WHERE price >= 200;"},
                {"id": "2.8", "text": {"en": "Get all employees hired <b>before</b> 2017.", "ru": "Выведи всех сотрудников, нанятых <b>до</b> 2017 года."},
                 "answer": "SELECT * FROM employees WHERE hire_year < 2017;"},
                # Section B
                {"id": "2.9", "section": {"en": "B · AND / OR / NOT", "ru": "B · AND / OR / NOT"},
                 "intro": {
                     "en": '''<p><code>AND</code> needs both conditions to be true, <code>OR</code> needs at least one, <code>NOT</code> turns a condition around. <code>AND</code> is applied before <code>OR</code>, so when you mix them, put the <code>OR</code> part in parentheses.</p>
<p><b>Example:</b> HR employees hired after 2018.</p>''',
                     "ru": '''<p><code>AND</code> требует, чтобы были верны оба условия, <code>OR</code> — хотя бы одно, <code>NOT</code> переворачивает условие. <code>AND</code> выполняется раньше <code>OR</code>, поэтому если они встречаются вместе, бери часть с <code>OR</code> в скобки.</p>
<p><b>Пример:</b> сотрудники HR, нанятые после 2018 года.</p>''',
                 },
                 "example": "SELECT first_name, department, hire_year\nFROM employees\nWHERE department = 'HR' AND hire_year > 2018;",
                 "text": {"en": "Get all IT employees with salary greater than 65000.", "ru": "Выведи всех сотрудников IT с зарплатой больше 65000."},
                 "answer": "SELECT * FROM employees WHERE department = 'IT' AND salary > 65000;"},
                {"id": "2.10", "text": {"en": "Get all employees from <code>'London'</code> OR <code>'Paris'</code>.", "ru": "Выведи всех сотрудников из <code>'London'</code> ИЛИ <code>'Paris'</code>."},
                 "answer": "SELECT * FROM employees WHERE city = 'London' OR city = 'Paris';"},
                {"id": "2.11", "text": {"en": "Get all employees from <code>'London'</code> or <code>'Paris'</code> <b>whose salary is above 50000</b>.", "ru": "Выведи всех сотрудников из <code>'London'</code> или <code>'Paris'</code> <b>с зарплатой выше 50000</b>."},
                 "answer": "SELECT * FROM employees\nWHERE (city = 'London' OR city = 'Paris') AND salary > 50000;"},
                {"id": "2.12", "text": {"en": "Get all products in the <code>'Electronics'</code> category with price below 500.", "ru": "Выведи все товары категории <code>'Electronics'</code> с ценой меньше 500."},
                 "answer": "SELECT * FROM products WHERE category = 'Electronics' AND price < 500;"},
                {"id": "2.13", "text": {"en": "Get all employees NOT in the <code>'HR'</code> department.", "ru": "Выведи всех сотрудников, которые НЕ работают в отделе <code>'HR'</code>."},
                 "answer": "SELECT * FROM employees WHERE NOT department = 'HR';"},
                {"id": "2.14", "text": {"en": "Get all products that are NOT in <code>'Stationery'</code> and cost more than 100.", "ru": "Выведи все товары НЕ из категории <code>'Stationery'</code> дороже 100."},
                 "answer": "SELECT * FROM products WHERE NOT category = 'Stationery' AND price > 100;"},
                # Section B+ (extra practice, added after task 10 caused trouble)
                {"id": "2.or1",
                 "section": {"en": "B+ · Practice: OR on one column", "ru": "B+ · Практика: OR по одному столбцу"},
                 "intro": {
                     "en": '''<p>To match one of several values in the <b>same column</b>, write the full condition on each side of <code>OR</code>: <code>city = 'London' OR city = 'Paris'</code>.</p>
<p>Two mistakes to avoid:</p>
<ul>
  <li><code>city = 'London' OR 'Paris'</code> — the part after <code>OR</code> is not a condition, so SQL quietly returns only London (3 rows instead of 6). No error, just a wrong answer.</li>
  <li><code>city = 'London' AND city = 'Paris'</code> — one row cannot be in two cities at once, so the result is empty.</li>
</ul>
<p><b>Example:</b> products from TechCorp or BrightHome.</p>''',
                     "ru": '''<p>Чтобы найти одно из нескольких значений в <b>одном и том же столбце</b>, пиши полное условие с каждой стороны <code>OR</code>: <code>city = 'London' OR city = 'Paris'</code>.</p>
<p>Две ошибки, которых стоит избегать:</p>
<ul>
  <li><code>city = 'London' OR 'Paris'</code> — после <code>OR</code> стоит не условие, поэтому SQL молча вернёт только London (3 строки вместо 6). Ошибки не будет, просто неверный ответ.</li>
  <li><code>city = 'London' AND city = 'Paris'</code> — строка не может быть сразу в двух городах, поэтому результат пустой.</li>
</ul>
<p><b>Пример:</b> товары от TechCorp или BrightHome.</p>''',
                 },
                 "example": "SELECT product_name, supplier\nFROM products\nWHERE supplier = 'TechCorp' OR supplier = 'BrightHome';",
                 "text": {"en": "Get all employees from <code>'Berlin'</code> OR <code>'Madrid'</code>.", "ru": "Выведи всех сотрудников из <code>'Berlin'</code> ИЛИ <code>'Madrid'</code>."},
                 "answer": "SELECT * FROM employees WHERE city = 'Berlin' OR city = 'Madrid';"},
                {"id": "2.or2", "text": {"en": "Get all employees who work in <code>'HR'</code> OR <code>'Sales'</code>.", "ru": "Выведи всех сотрудников отделов <code>'HR'</code> ИЛИ <code>'Sales'</code>."},
                 "answer": "SELECT * FROM employees WHERE department = 'HR' OR department = 'Sales';"},
                {"id": "2.or3", "text": {"en": "Get all employees hired in 2018 OR 2020.", "ru": "Выведи всех сотрудников, нанятых в 2018 ИЛИ 2020 году."},
                 "answer": "SELECT * FROM employees WHERE hire_year = 2018 OR hire_year = 2020;"},
                {"id": "2.or4", "text": {"en": "Get all products in the <code>'Furniture'</code> OR <code>'Stationery'</code> category.", "ru": "Выведи все товары категории <code>'Furniture'</code> ИЛИ <code>'Stationery'</code>."},
                 "answer": "SELECT * FROM products WHERE category = 'Furniture' OR category = 'Stationery';"},
                {"id": "2.or5", "text": {"en": "Get all products from the supplier <code>'GadgetInc'</code> OR <code>'ComfortPlus'</code>.", "ru": "Выведи все товары поставщика <code>'GadgetInc'</code> ИЛИ <code>'ComfortPlus'</code>."},
                 "answer": "SELECT * FROM products WHERE supplier = 'GadgetInc' OR supplier = 'ComfortPlus';"},
                {"id": "2.or6", "text": {"en": "Get the employees whose first name is <code>'Alice'</code> OR <code>'Bob'</code>.", "ru": "Выведи сотрудников, которых зовут <code>'Alice'</code> ИЛИ <code>'Bob'</code>."},
                 "answer": "SELECT * FROM employees WHERE first_name = 'Alice' OR first_name = 'Bob';"},
                {"id": "2.or7", "text": {"en": "Get all employees whose salary is exactly 45000 OR 55000.", "ru": "Выведи всех сотрудников с зарплатой ровно 45000 ИЛИ 55000."},
                 "answer": "SELECT * FROM employees WHERE salary = 45000 OR salary = 55000;"},
                {"id": "2.or8", "text": {"en": "Get all employees from <code>'London'</code>, <code>'Paris'</code> OR <code>'Berlin'</code> (three values, use <code>OR</code> twice).", "ru": "Выведи всех сотрудников из <code>'London'</code>, <code>'Paris'</code> ИЛИ <code>'Berlin'</code> (три значения, два раза <code>OR</code>)."},
                 "answer": "SELECT * FROM employees WHERE city = 'London' OR city = 'Paris' OR city = 'Berlin';"},
                {"id": "2.or9", "text": {"en": "Show <code>product_name</code> and <code>stock</code> of the products whose stock is 15 OR 20.", "ru": "Покажи <code>product_name</code> и <code>stock</code> товаров, у которых <code>stock</code> равен 15 ИЛИ 20."},
                 "answer": "SELECT product_name, stock FROM products WHERE stock = 15 OR stock = 20;"},
                {"id": "2.or10", "text": {"en": "Show <code>first_name</code>, <code>last_name</code> and <code>city</code> of the employees whose last name is <code>'Smith'</code> OR <code>'Davis'</code>.", "ru": "Покажи <code>first_name</code>, <code>last_name</code> и <code>city</code> сотрудников с фамилией <code>'Smith'</code> ИЛИ <code>'Davis'</code>."},
                 "answer": "SELECT first_name, last_name, city FROM employees WHERE last_name = 'Smith' OR last_name = 'Davis';"},
                # Section B++ (added after the "Paris OR 'Berlin' AND salary" mistake)
                {"id": "2.p1",
                 "section": {"en": "B++ · Practice: AND with OR, use brackets", "ru": "B++ · Практика: AND вместе с OR, нужны скобки"},
                 "intro": {"en": '''<p>"Employees from Paris or Berlin with salary above 50000" has two parts: <b>which city</b> (Paris or Berlin) and <b>which salary</b> (above 50000). Both parts must be true, so the city part has to be one group.</p>
<p><b>Why <code>city = 'Paris' OR 'Berlin' AND salary &gt; 50000</code> is wrong.</b> It has two separate problems:</p>
<ol>
  <li><b><code>'Berlin'</code> on its own is not a condition.</b> It is just a piece of text, and nothing compares it with <code>city</code>. In this trainer such text counts as false, so the Berlin part never matches anyone (some databases give an error instead). You have to write <code>city = 'Berlin'</code>.</li>
  <li><b><code>AND</code> is worked out before <code>OR</code></b>, the way × comes before + in maths. So SQL reads the condition as <code>city = 'Paris' OR ('Berlin' AND salary &gt; 50000)</code>, and every employee from Paris passes, whatever their salary.</li>
</ol>
<p>Even with both comparisons written out, <code>city = 'Paris' OR city = 'Berlin' AND salary &gt; 50000</code> is still wrong. It means "everyone from Paris, plus the people from Berlin who earn more than 50000".</p>
<table class="ops"><thead><tr><th>Condition</th><th>Rows</th><th>Who</th></tr></thead><tbody>
<tr><td><code>city = 'Paris' OR 'Berlin' AND salary &gt; 50000</code></td><td>3</td><td>Bob, Ethan, Julia: all of Paris, even Bob (45000) and Julia (41000)</td></tr>
<tr><td><code>city = 'Paris' OR city = 'Berlin' AND salary &gt; 50000</code></td><td>5</td><td>Bob, Ethan, Julia, Diana, George</td></tr>
<tr><td><code>(city = 'Paris' OR city = 'Berlin') AND salary &gt; 50000</code></td><td>3</td><td>Ethan, Diana, George ✓</td></tr>
</tbody></table>
<p>The first wrong version also returns 3 rows, but they are the wrong people. Always check <b>who</b> is in the result, not only how many rows there are.</p>
<p><b>Why the brackets fix it.</b> Brackets are worked out first, as in maths. <code>(city = 'Paris' OR city = 'Berlin')</code> becomes one yes-or-no answer, "is the city Paris or Berlin?", and only then <code>AND salary &gt; 50000</code> is applied to it.</p>
<p><b>Rule:</b> whenever a condition has both <code>AND</code> and <code>OR</code>, put the <code>OR</code> part in brackets. <code>A OR B AND C</code> works like <code>a + b × c</code>, which is <code>a + (b × c)</code>, not <code>(a + b) × c</code>.</p>
<p><b>Example:</b> the correct query from the table.</p>''', "ru": '''<p>«Сотрудники из Парижа или Берлина с зарплатой выше 50000» состоит из двух частей: <b>какой город</b> (Париж или Берлин) и <b>какая зарплата</b> (выше 50000). Обе части должны выполняться, поэтому часть про город должна быть одной группой.</p>
<p><b>Почему <code>city = 'Paris' OR 'Berlin' AND salary &gt; 50000</code> неверно.</b> Здесь две отдельные ошибки:</p>
<ol>
  <li><b><code>'Berlin'</code> сам по себе не условие.</b> Это просто текст, его ни с чем не сравнивают. В этом тренажёре такой текст считается ложью, поэтому часть про Берлин не находит никого (в некоторых СУБД будет ошибка). Нужно писать <code>city = 'Berlin'</code>.</li>
  <li><b><code>AND</code> выполняется раньше <code>OR</code></b>, как умножение раньше сложения. Поэтому SQL читает условие как <code>city = 'Paris' OR ('Berlin' AND salary &gt; 50000)</code>, и проходят все сотрудники из Парижа, с любой зарплатой.</li>
</ol>
<p>Даже если написать оба сравнения полностью, <code>city = 'Paris' OR city = 'Berlin' AND salary &gt; 50000</code> всё равно неверно. Это значит «все из Парижа плюс те из Берлина, кто получает больше 50000».</p>
<table class="ops"><thead><tr><th>Условие</th><th>Строк</th><th>Кто</th></tr></thead><tbody>
<tr><td><code>city = 'Paris' OR 'Berlin' AND salary &gt; 50000</code></td><td>3</td><td>Bob, Ethan, Julia: весь Париж, даже Bob (45000) и Julia (41000)</td></tr>
<tr><td><code>city = 'Paris' OR city = 'Berlin' AND salary &gt; 50000</code></td><td>5</td><td>Bob, Ethan, Julia, Diana, George</td></tr>
<tr><td><code>(city = 'Paris' OR city = 'Berlin') AND salary &gt; 50000</code></td><td>3</td><td>Ethan, Diana, George ✓</td></tr>
</tbody></table>
<p>Первый неверный вариант тоже возвращает 3 строки, но не тех людей. Всегда смотри, <b>кто</b> попал в результат, а не только сколько строк.</p>
<p><b>Почему скобки всё исправляют.</b> Скобки выполняются первыми, как в математике. <code>(city = 'Paris' OR city = 'Berlin')</code> превращается в один ответ «да или нет»: «город Париж или Берлин?», и только потом к нему применяется <code>AND salary &gt; 50000</code>.</p>
<p><b>Правило:</b> если в условии есть и <code>AND</code>, и <code>OR</code>, бери часть с <code>OR</code> в скобки. <code>A OR B AND C</code> работает как <code>a + b × c</code>, то есть <code>a + (b × c)</code>, а не <code>(a + b) × c</code>.</p>
<p><b>Пример:</b> правильный запрос из таблицы.</p>'''},
                 "example": "SELECT first_name, city, salary\nFROM employees\nWHERE (city = 'Paris' OR city = 'Berlin') AND salary > 50000;",
                 "text": {"en": "Get all employees from <code>'Paris'</code> OR <code>'Berlin'</code> with salary above 50000. This is the task that caused trouble: now write it with brackets.", "ru": "Выведи всех сотрудников из <code>'Paris'</code> ИЛИ <code>'Berlin'</code> с зарплатой выше 50000. Это то самое задание, на котором была ошибка: теперь напиши его со скобками."},
                 "answer": "SELECT * FROM employees\nWHERE (city = 'Paris' OR city = 'Berlin') AND salary > 50000;"},
                {"id": "2.p2",
                 "text": {"en": "Get all employees from <code>'Sales'</code> OR <code>'HR'</code> with salary above 50000.", "ru": "Выведи всех сотрудников отделов <code>'Sales'</code> ИЛИ <code>'HR'</code> с зарплатой выше 50000."},
                 "answer": "SELECT * FROM employees\nWHERE (department = 'Sales' OR department = 'HR') AND salary > 50000;"},
                {"id": "2.p3",
                 "text": {"en": "Get all employees with salary greater than 60000 who work in <code>'IT'</code> OR <code>'Sales'</code>.", "ru": "Выведи всех сотрудников с зарплатой больше 60000, которые работают в <code>'IT'</code> ИЛИ <code>'Sales'</code>."},
                 "answer": "SELECT * FROM employees\nWHERE salary > 60000 AND (department = 'IT' OR department = 'Sales');"},
                {"id": "2.p4",
                 "text": {"en": "Get all employees from <code>'London'</code> OR <code>'Madrid'</code> hired after 2016.", "ru": "Выведи всех сотрудников из <code>'London'</code> ИЛИ <code>'Madrid'</code>, нанятых после 2016 года."},
                 "answer": "SELECT * FROM employees\nWHERE (city = 'London' OR city = 'Madrid') AND hire_year > 2016;"},
                {"id": "2.p5",
                 "text": {"en": "Get all employees from <code>'HR'</code> OR <code>'Sales'</code> who have a bonus.", "ru": "Выведи всех сотрудников отделов <code>'HR'</code> ИЛИ <code>'Sales'</code>, у которых есть бонус."},
                 "answer": "SELECT * FROM employees\nWHERE (department = 'HR' OR department = 'Sales') AND bonus IS NOT NULL;"},
                {"id": "2.p6",
                 "text": {"en": "Get all employees from <code>'Paris'</code> OR <code>'Berlin'</code> whose salary is <code>BETWEEN</code> 45000 <code>AND</code> 60000.", "ru": "Выведи всех сотрудников из <code>'Paris'</code> ИЛИ <code>'Berlin'</code> с зарплатой <code>BETWEEN</code> 45000 <code>AND</code> 60000."},
                 "answer": "SELECT * FROM employees\nWHERE (city = 'Paris' OR city = 'Berlin')\n  AND salary BETWEEN 45000 AND 60000;"},
                {"id": "2.p7",
                 "text": {"en": "Get all employees whose first name starts with <code>'J'</code> OR last name starts with <code>'P'</code>, and whose salary is above 55000.", "ru": "Выведи всех сотрудников, у которых имя начинается на <code>'J'</code> ИЛИ фамилия на <code>'P'</code>, а зарплата выше 55000."},
                 "answer": "SELECT * FROM employees\nWHERE (first_name LIKE 'J%' OR last_name LIKE 'P%') AND salary > 55000;"},
                {"id": "2.p8",
                 "text": {"en": "Get all employees from <code>'HR'</code> OR <code>'Sales'</code> whose salary is <code>NOT BETWEEN</code> 45000 <code>AND</code> 55000.", "ru": "Выведи всех сотрудников отделов <code>'HR'</code> ИЛИ <code>'Sales'</code> с зарплатой <code>NOT BETWEEN</code> 45000 <code>AND</code> 55000."},
                 "answer": "SELECT * FROM employees\nWHERE (department = 'HR' OR department = 'Sales')\n  AND salary NOT BETWEEN 45000 AND 55000;"},
                {"id": "2.p9",
                 "text": {"en": "Get all employees from <code>'London'</code> OR <code>'Berlin'</code> who work in <code>'IT'</code> OR <code>'Sales'</code>. Two groups, two pairs of brackets.", "ru": "Выведи всех сотрудников из <code>'London'</code> ИЛИ <code>'Berlin'</code>, которые работают в <code>'IT'</code> ИЛИ <code>'Sales'</code>. Две группы — две пары скобок."},
                 "answer": "SELECT * FROM employees\nWHERE (city = 'London' OR city = 'Berlin')\n  AND (department = 'IT' OR department = 'Sales');"},
                {"id": "2.p10",
                 "text": {"en": "Fix the bug. This query should return IT and Sales employees who earn more than 60000, but it returns every IT employee whatever the salary: <code>SELECT * FROM employees WHERE department = 'IT' OR department = 'Sales' AND salary &gt; 60000;</code> Write the correct query.", "ru": "Найди ошибку. Этот запрос должен вернуть сотрудников IT и Sales с зарплатой больше 60000, но возвращает всех сотрудников IT с любой зарплатой: <code>SELECT * FROM employees WHERE department = 'IT' OR department = 'Sales' AND salary &gt; 60000;</code> Напиши правильный запрос."},
                 "answer": "SELECT * FROM employees\nWHERE (department = 'IT' OR department = 'Sales') AND salary > 60000;"},
                # Section B+++ (operator order: NOT, then AND, then OR)
                {"id": "2.o1",
                 "kind": "row",
                 "row": 2,
                 "section": {"en": "B+++ · Who goes first: NOT, AND, OR", "ru": "B+++ · Кто первый: NOT, AND, OR"},
                 "intro": {"en": '''<p>When a condition mixes <code>NOT</code>, <code>AND</code> and <code>OR</code>, SQL works them out in a fixed order, the way × comes before + in maths:</p>
<table class="ops"><thead><tr><th>Order</th><th>Operator</th><th>What it takes</th></tr></thead><tbody>
<tr><td>1</td><td><code>NOT</code></td><td>only the one condition right after it</td></tr>
<tr><td>2</td><td><code>AND</code></td><td>the condition on its left and the one on its right</td></tr>
<tr><td>3</td><td><code>OR</code></td><td>whatever is left, last of all</td></tr>
</tbody></table>
<p>So <code>A OR B AND C</code> means <code>A OR (B AND C)</code>, and <code>NOT A AND B</code> means <code>(NOT A) AND B</code>. Brackets change the order: whatever is inside them is worked out first, as in maths.</p>
<p><b>Reminder:</b> <code>AND</code> is true only when both sides are true. <code>OR</code> is true when at least one side is true. <code>NOT</code> turns true into false and false into true.</p>
<table class="ops"><thead><tr><th>A</th><th>B</th><th>A AND B</th><th>A OR B</th><th>NOT A</th></tr></thead><tbody>
<tr><td>true</td><td>true</td><td>true</td><td>true</td><td>false</td></tr>
<tr><td>true</td><td>false</td><td>false</td><td>true</td><td>false</td></tr>
<tr><td>false</td><td>true</td><td>false</td><td>true</td><td>true</td></tr>
<tr><td>false</td><td>false</td><td>false</td><td>false</td><td>true</td></tr>
</tbody></table>
<p><b>Two traps:</b></p>
<ol>
  <li><b><code>OR</code> takes too much.</b> <code>city = 'Paris' OR city = 'Berlin' AND salary &gt; 50000</code> is read as <code>city = 'Paris' OR (city = 'Berlin' AND salary &gt; 50000)</code>: everyone from Paris passes, and the salary is checked only for Berlin.</li>
  <li><b><code>NOT</code> takes too little.</b> <code>NOT city = 'Paris' OR city = 'Berlin'</code> is read as <code>(NOT city = 'Paris') OR city = 'Berlin'</code>: everyone who is not from Paris, Berlin included. To turn the whole group around, put it in brackets: <code>NOT (city = 'Paris' OR city = 'Berlin')</code>.</li>
</ol>
<p><b>Rules:</b> if a condition has both <code>AND</code> and <code>OR</code>, put the <code>OR</code> part in brackets. If <code>NOT</code> is meant for more than one condition, put brackets right after <code>NOT</code>.</p>
<p><b>The tasks:</b> first decide whether one person passes a condition, then mark everyone who passes a query, then write the queries yourself.</p>
<p><b>Example:</b> <code>NOT</code> here takes only <code>department = 'IT'</code>, so this means "not in IT, and salary above 50000".</p>''', "ru": '''<p>Когда в условии встречаются <code>NOT</code>, <code>AND</code> и <code>OR</code>, SQL выполняет их в постоянном порядке, как умножение раньше сложения:</p>
<table class="ops"><thead><tr><th>Порядок</th><th>Оператор</th><th>Что он берёт</th></tr></thead><tbody>
<tr><td>1</td><td><code>NOT</code></td><td>только одно условие сразу после себя</td></tr>
<tr><td>2</td><td><code>AND</code></td><td>условие слева и условие справа</td></tr>
<tr><td>3</td><td><code>OR</code></td><td>всё, что осталось, в самом конце</td></tr>
</tbody></table>
<p>Поэтому <code>A OR B AND C</code> значит <code>A OR (B AND C)</code>, а <code>NOT A AND B</code> значит <code>(NOT A) AND B</code>. Скобки меняют порядок: то, что внутри, выполняется первым, как в математике.</p>
<p><b>Напоминание:</b> <code>AND</code> верно, только когда верны обе стороны. <code>OR</code> верно, когда верна хотя бы одна. <code>NOT</code> меняет «верно» на «неверно» и наоборот.</p>
<table class="ops"><thead><tr><th>A</th><th>B</th><th>A AND B</th><th>A OR B</th><th>NOT A</th></tr></thead><tbody>
<tr><td>верно</td><td>верно</td><td>верно</td><td>верно</td><td>неверно</td></tr>
<tr><td>верно</td><td>неверно</td><td>неверно</td><td>верно</td><td>неверно</td></tr>
<tr><td>неверно</td><td>верно</td><td>неверно</td><td>верно</td><td>верно</td></tr>
<tr><td>неверно</td><td>неверно</td><td>неверно</td><td>неверно</td><td>верно</td></tr>
</tbody></table>
<p><b>Две ловушки:</b></p>
<ol>
  <li><b><code>OR</code> забирает слишком много.</b> <code>city = 'Paris' OR city = 'Berlin' AND salary &gt; 50000</code> читается как <code>city = 'Paris' OR (city = 'Berlin' AND salary &gt; 50000)</code>: проходят все из Парижа, а зарплата проверяется только у берлинцев.</li>
  <li><b><code>NOT</code> забирает слишком мало.</b> <code>NOT city = 'Paris' OR city = 'Berlin'</code> читается как <code>(NOT city = 'Paris') OR city = 'Berlin'</code>: все, кто не из Парижа, включая Берлин. Чтобы перевернуть всю группу, возьми её в скобки: <code>NOT (city = 'Paris' OR city = 'Berlin')</code>.</li>
</ol>
<p><b>Правила:</b> если в условии есть и <code>AND</code>, и <code>OR</code>, бери часть с <code>OR</code> в скобки. Если <code>NOT</code> относится к нескольким условиям, ставь скобки сразу после <code>NOT</code>.</p>
<p><b>Задания:</b> сначала реши, пройдёт ли условие один конкретный человек, потом отметь всех, кто попадёт в результат запроса, и в конце напиши запросы сам.</p>
<p><b>Пример:</b> здесь <code>NOT</code> берёт только <code>department = 'IT'</code>, то есть «не из IT, и зарплата выше 50000».</p>'''},
                 "example": "SELECT first_name, department, salary\nFROM employees\nWHERE NOT department = 'IT' AND salary > 50000;",
                 "condition": "city = 'Paris' OR city = 'Berlin' AND salary > 50000",
                 "text": {"en": "Will <b>Bob</b> be in the result of this condition?", "ru": "Попадёт ли <b>Bob</b> в результат этого условия?"},
                 "explain": {"en": "Yes. <code>AND</code> goes first, so this is <code>city = 'Paris' OR (city = 'Berlin' AND salary &gt; 50000)</code>. Bob is from Paris, so the left side is already true, and his salary is never checked.", "ru": "Да. <code>AND</code> выполняется первым, поэтому это <code>city = 'Paris' OR (city = 'Berlin' AND salary &gt; 50000)</code>. Боб из Парижа, левая часть уже верна, и его зарплату никто не проверяет."}},
                {"id": "2.o2",
                 "kind": "row",
                 "row": 8,
                 "condition": "department = 'IT' AND (city = 'London' OR salary > 60000)",
                 "text": {"en": "Will <b>Hannah</b> be in the result of this condition?", "ru": "Попадёт ли <b>Hannah</b> в результат этого условия?"},
                 "explain": {"en": "No. The brackets go first: <code>(city = 'London' OR salary &gt; 60000)</code> is true for Hannah. But she is in Sales, so <code>department = 'IT'</code> is false, and false <code>AND</code> anything is false. Without the brackets the answer would be Yes: <code>(department = 'IT' AND city = 'London') OR salary &gt; 60000</code>.", "ru": "Нет. Скобки выполняются первыми: <code>(city = 'London' OR salary &gt; 60000)</code> для Ханны верно. Но она в Sales, поэтому <code>department = 'IT'</code> неверно, а «неверно <code>AND</code> что угодно» — неверно. Без скобок ответ был бы «Да»: <code>(department = 'IT' AND city = 'London') OR salary &gt; 60000</code>."}},
                {"id": "2.o3",
                 "kind": "row",
                 "row": 5,
                 "condition": "NOT department = 'HR' AND salary > 60000",
                 "text": {"en": "Will <b>Ethan</b> be in the result of this condition?", "ru": "Попадёт ли <b>Ethan</b> в результат этого условия?"},
                 "explain": {"en": "Yes. <code>NOT</code> takes only the condition right after it: <code>(NOT department = 'HR') AND salary &gt; 60000</code>. Ethan is in IT, so <code>NOT department = 'HR'</code> is true, and 68000 is more than 60000.", "ru": "Да. <code>NOT</code> берёт только условие сразу после себя: <code>(NOT department = 'HR') AND salary &gt; 60000</code>. Итан в IT, поэтому <code>NOT department = 'HR'</code> верно, и 68000 больше 60000."}},
                {"id": "2.o4",
                 "kind": "row",
                 "row": 2,
                 "condition": "NOT (department = 'HR' AND salary > 60000)",
                 "text": {"en": "Will <b>Bob</b> be in the result of this condition?", "ru": "Попадёт ли <b>Bob</b> в результат этого условия?"},
                 "explain": {"en": "Yes, and that surprises many people. Here <code>NOT</code> takes the whole group. Inside it, Bob is in HR (true) but earns 45000, so <code>salary &gt; 60000</code> is false, and true <code>AND</code> false is false. <code>NOT</code> false is true, so Bob is in the result. This condition removes only HR people who earn more than 60000, and there are none.", "ru": "Да, и это многих удивляет. Здесь <code>NOT</code> берёт всю группу. Внутри: Боб в HR (верно), но получает 45000, поэтому <code>salary &gt; 60000</code> неверно, а «верно <code>AND</code> неверно» — неверно. <code>NOT</code> от «неверно» — «верно», и Боб попадает в результат. Это условие убирает только сотрудников HR с зарплатой больше 60000, а таких нет."}},
                {"id": "2.o5",
                 "kind": "row",
                 "row": 5,
                 "condition": "NOT (city = 'Paris' OR department = 'HR')",
                 "text": {"en": "Will <b>Ethan</b> be in the result of this condition?", "ru": "Попадёт ли <b>Ethan</b> в результат этого условия?"},
                 "explain": {"en": "No. Inside the brackets: Ethan is from Paris, so <code>city = 'Paris' OR department = 'HR'</code> is true. <code>NOT</code> true is false, so Ethan is not in the result.", "ru": "Нет. Внутри скобок: Итан из Парижа, поэтому <code>city = 'Paris' OR department = 'HR'</code> верно. <code>NOT</code> от «верно» — «неверно», и Итана в результате нет."}},
                {"id": "2.o6",
                 "kind": "pick",
                 "condition": "city = 'Berlin' OR city = 'Paris' AND salary > 55000",
                 "text": {"en": "Mark everyone who will be in the result of this query, then press <b>Check</b>.", "ru": "Отметь всех, кто попадёт в результат этого запроса, и нажми <b>Проверить</b>."},
                 "explain": {"en": "<code>AND</code> goes first: <code>city = 'Berlin' OR (city = 'Paris' AND salary &gt; 55000)</code>. Both people from Berlin pass, Diana and George, whatever their salary. From Paris only Ethan earns more than 55000.", "ru": "<code>AND</code> выполняется первым: <code>city = 'Berlin' OR (city = 'Paris' AND salary &gt; 55000)</code>. Проходят оба берлинца, Диана и Джордж, с любой зарплатой. Из Парижа только Итан получает больше 55000."}},
                {"id": "2.o7",
                 "kind": "pick",
                 "condition": "(city = 'Berlin' OR city = 'Paris') AND salary > 55000",
                 "text": {"en": "Mark everyone who will be in the result of this query, then press <b>Check</b>. Compare with the previous task.", "ru": "Отметь всех, кто попадёт в результат этого запроса, и нажми <b>Проверить</b>. Сравни с предыдущим заданием."},
                 "explain": {"en": "The brackets go first: from Berlin or Paris, <b>and</b> salary above 55000. Diana earns 52000 and George exactly 55000, which is not more than 55000. Only Ethan is left. The same words as in the previous task, a different result.", "ru": "Скобки выполняются первыми: из Берлина или Парижа, <b>и</b> зарплата выше 55000. Диана получает 52000, а Джордж ровно 55000, это не больше 55000. Остаётся только Итан. Те же слова, что в прошлом задании, а результат другой."}},
                {"id": "2.o8",
                 "kind": "pick",
                 "condition": "department = 'IT' OR department = 'Sales' AND bonus > 5000",
                 "text": {"en": "Mark everyone who will be in the result of this query, then press <b>Check</b>.", "ru": "Отметь всех, кто попадёт в результат этого запроса, и нажми <b>Проверить</b>."},
                 "explain": {"en": "<code>AND</code> goes first: <code>department = 'IT' OR (department = 'Sales' AND bonus &gt; 5000)</code>. All four IT people pass: Alice, Charlie, Ethan, Ivan. From Sales only Hannah has a bonus above 5000.", "ru": "<code>AND</code> выполняется первым: <code>department = 'IT' OR (department = 'Sales' AND bonus &gt; 5000)</code>. Проходят все четверо из IT: Элис, Чарли, Итан, Иван. Из Sales бонус больше 5000 только у Ханны."}},
                {"id": "2.o9",
                 "kind": "pick",
                 "condition": "department = 'IT' OR (department = 'Sales' AND bonus > 5000)",
                 "text": {"en": "Mark everyone who will be in the result of this query, then press <b>Check</b>. Compare with the previous task.", "ru": "Отметь всех, кто попадёт в результат этого запроса, и нажми <b>Проверить</b>. Сравни с предыдущим заданием."},
                 "explain": {"en": "These brackets put <code>AND</code> first, exactly as SQL does anyway, so the result is the same as in the previous task: Alice, Charlie, Ethan, Hannah, Ivan. Brackets that repeat the normal order change nothing, but they make the query easier to read.", "ru": "Эти скобки ставят <code>AND</code> первым, как SQL и так делает, поэтому результат тот же, что в прошлом задании: Элис, Чарли, Итан, Ханна, Иван. Скобки, повторяющие обычный порядок, ничего не меняют, но делают запрос понятнее."}},
                {"id": "2.o10",
                 "kind": "pick",
                 "condition": "NOT department = 'HR' AND salary > 60000",
                 "text": {"en": "Mark everyone who will be in the result of this query, then press <b>Check</b>.", "ru": "Отметь всех, кто попадёт в результат этого запроса, и нажми <b>Проверить</b>."},
                 "explain": {"en": "<code>NOT</code> takes only <code>department = 'HR'</code>: <code>(NOT department = 'HR') AND salary &gt; 60000</code>. These are people outside HR who earn more than 60000: Charlie, Ethan, Hannah, Ivan. Alice earns exactly 60000, which is not more.", "ru": "<code>NOT</code> берёт только <code>department = 'HR'</code>: <code>(NOT department = 'HR') AND salary &gt; 60000</code>. Это люди не из HR с зарплатой больше 60000: Чарли, Итан, Ханна, Иван. Элис получает ровно 60000, это не больше."}},
                {"id": "2.o11",
                 "kind": "pick",
                 "condition": "NOT (department = 'HR' AND salary > 60000)",
                 "text": {"en": "Mark everyone who will be in the result of this query, then press <b>Check</b>. Compare with the previous task.", "ru": "Отметь всех, кто попадёт в результат этого запроса, и нажми <b>Проверить</b>. Сравни с предыдущим заданием."},
                 "explain": {"en": "<code>NOT</code> takes the whole group. The group is true only for HR people who earn more than 60000, and there are none. So the group is false for everyone, <code>NOT</code> makes it true, and all 10 employees are in the result.", "ru": "<code>NOT</code> берёт всю группу. Группа верна только для сотрудников HR с зарплатой больше 60000, а таких нет. Значит, для всех она неверна, <code>NOT</code> делает её верной, и в результате все 10 сотрудников."}},
                {"id": "2.o12",
                 "kind": "pick",
                 "condition": "NOT department = 'HR' OR salary > 60000",
                 "text": {"en": "Mark everyone who will be in the result of this query, then press <b>Check</b>.", "ru": "Отметь всех, кто попадёт в результат этого запроса, и нажми <b>Проверить</b>."},
                 "explain": {"en": "<code>(NOT department = 'HR') OR salary &gt; 60000</code>: everyone outside HR passes (Alice, Charlie, Diana, Ethan, Fiona, Hannah, Ivan), plus anyone in HR who earns more than 60000, and there is nobody like that. Bob, George and Julia are left out.", "ru": "<code>(NOT department = 'HR') OR salary &gt; 60000</code>: проходят все не из HR (Элис, Чарли, Диана, Итан, Фиона, Ханна, Иван) плюс сотрудники HR с зарплатой больше 60000, а таких нет. Боб, Джордж и Джулия не попадают."}},
                {"id": "2.o13",
                 "text": {"en": "Get all employees who are from neither <code>'London'</code> nor <code>'Madrid'</code>. Put <code>NOT</code> in front of a group in brackets.", "ru": "Выведи всех сотрудников, которые не из <code>'London'</code> и не из <code>'Madrid'</code>. Поставь <code>NOT</code> перед группой в скобках."},
                 "answer": "SELECT * FROM employees\nWHERE NOT (city = 'London' OR city = 'Madrid');"},
                {"id": "2.o14",
                 "text": {"en": "Fix the query. It should return the employees who are <b>not in IT</b> and earn more than 60000, but it returns 7 people: <code>SELECT * FROM employees WHERE NOT (department = 'IT' AND salary &gt; 60000);</code>", "ru": "Исправь запрос. Он должен вернуть сотрудников <b>не из IT</b> с зарплатой больше 60000, а возвращает 7 человек: <code>SELECT * FROM employees WHERE NOT (department = 'IT' AND salary &gt; 60000);</code>"},
                 "answer": "SELECT * FROM employees\nWHERE department <> 'IT' AND salary > 60000;"},
                {"id": "2.o15",
                 "text": {"en": "Fix the query. It should return <b>Sales</b> employees whose bonus is missing or below 3000, but it also returns people from other departments: <code>SELECT * FROM employees WHERE bonus IS NULL OR bonus &lt; 3000 AND department = 'Sales';</code>", "ru": "Исправь запрос. Он должен вернуть сотрудников <b>Sales</b>, у которых бонуса нет или он меньше 3000, а возвращает и людей из других отделов: <code>SELECT * FROM employees WHERE bonus IS NULL OR bonus &lt; 3000 AND department = 'Sales';</code>"},
                 "answer": "SELECT * FROM employees\nWHERE department = 'Sales' AND (bonus IS NULL OR bonus < 3000);"},
                {"id": "2.o16",
                 "text": {"en": "Get the employees who are either in IT with salary above 70000, or in Sales, but only those hired after 2015. You need brackets inside brackets.", "ru": "Выведи сотрудников, которые либо из IT с зарплатой выше 70000, либо из Sales, но только нанятых после 2015 года. Понадобятся скобки внутри скобок."},
                 "answer": "SELECT * FROM employees\nWHERE ((department = 'IT' AND salary > 70000) OR department = 'Sales')\n  AND hire_year > 2015;"},
                # Section B++++ (De Morgan's laws)
                {"id": "2.d1",
                 "section": {"en": "B++++ · De Morgan's laws", "ru": "B++++ · Законы де Моргана"},
                 "intro": {"en": '''<p>De Morgan's laws show how to remove the brackets after <code>NOT</code>:</p>
<pre class="code">NOT (A OR B)   =   NOT A AND NOT B
NOT (A AND B)  =   NOT A OR  NOT B</pre>
<p><b>Recipe:</b> put <code>NOT</code> on each condition <b>and swap</b> <code>AND</code> ↔ <code>OR</code>.</p>
<p>In everyday words: "not (from Paris or from Berlin)" is "not from Paris <b>and</b> not from Berlin". "Not (from Paris and in HR)" is "not from Paris <b>or</b> not in HR".</p>
<p><code>NOT</code> in front of one comparison is usually written with the opposite operator: <code>NOT city = 'Paris'</code> is <code>city &lt;&gt; 'Paris'</code>, <code>NOT salary &gt; 50000</code> is <code>salary &lt;= 50000</code>, <code>NOT hire_year &lt; 2016</code> is <code>hire_year &gt;= 2016</code>.</p>
<p><b>The classic mistake is to forget the swap:</b></p>
<table class="ops"><thead><tr><th>Condition</th><th>Rows</th></tr></thead><tbody>
<tr><td><code>NOT (city = 'Paris' OR city = 'Berlin')</code></td><td>5</td></tr>
<tr><td><code>city &lt;&gt; 'Paris' AND city &lt;&gt; 'Berlin'</code></td><td>5 ✓ the same</td></tr>
<tr><td><code>city &lt;&gt; 'Paris' OR city &lt;&gt; 'Berlin'</code></td><td>10: everyone! Each person is either not in Paris or not in Berlin.</td></tr>
</tbody></table>
<p><code>NOT IN</code> is the same law in short form: <code>city NOT IN ('Paris', 'Berlin')</code> also returns those 5 people.</p>
<p><b>Example:</b> the second row of the table.</p>''', "ru": '''<p>Законы де Моргана показывают, как убрать скобки после <code>NOT</code>:</p>
<pre class="code">NOT (A OR B)   =   NOT A AND NOT B
NOT (A AND B)  =   NOT A OR  NOT B</pre>
<p><b>Рецепт:</b> поставь <code>NOT</code> перед каждым условием <b>и поменяй</b> <code>AND</code> ↔ <code>OR</code>.</p>
<p>Обычными словами: «не (из Парижа или из Берлина)» — это «не из Парижа <b>и</b> не из Берлина». «Не (из Парижа и в HR)» — это «не из Парижа <b>или</b> не в HR».</p>
<p><code>NOT</code> перед одним сравнением обычно записывают противоположным оператором: <code>NOT city = 'Paris'</code> — это <code>city &lt;&gt; 'Paris'</code>, <code>NOT salary &gt; 50000</code> — это <code>salary &lt;= 50000</code>, <code>NOT hire_year &lt; 2016</code> — это <code>hire_year &gt;= 2016</code>.</p>
<p><b>Классическая ошибка — забыть поменять AND и OR:</b></p>
<table class="ops"><thead><tr><th>Условие</th><th>Строк</th></tr></thead><tbody>
<tr><td><code>NOT (city = 'Paris' OR city = 'Berlin')</code></td><td>5</td></tr>
<tr><td><code>city &lt;&gt; 'Paris' AND city &lt;&gt; 'Berlin'</code></td><td>5 ✓ то же самое</td></tr>
<tr><td><code>city &lt;&gt; 'Paris' OR city &lt;&gt; 'Berlin'</code></td><td>10: все! Любой человек либо не в Париже, либо не в Берлине.</td></tr>
</tbody></table>
<p><code>NOT IN</code> — тот же закон в короткой записи: <code>city NOT IN ('Paris', 'Berlin')</code> тоже возвращает этих 5 человек.</p>
<p><b>Пример:</b> вторая строка таблицы.</p>'''},
                 "example": "SELECT first_name, city\nFROM employees\nWHERE city <> 'Paris' AND city <> 'Berlin';",
                 "text": {"en": "Get all employees who are in neither <code>'HR'</code> nor <code>'Sales'</code>. Write it <b>without</b> <code>NOT</code>, with <code>&lt;&gt;</code> twice. Which word goes between them?", "ru": "Выведи всех сотрудников, которые не в <code>'HR'</code> и не в <code>'Sales'</code>. Напиши <b>без</b> <code>NOT</code>, дважды через <code>&lt;&gt;</code>. Какое слово поставить между ними?"},
                 "answer": "SELECT * FROM employees\nWHERE department <> 'HR' AND department <> 'Sales';"},
                {"id": "2.d2",
                 "text": {"en": "Get all employees except those who are both from <code>'Paris'</code> and in <code>'HR'</code>. Use <code>NOT ( … AND … )</code>.", "ru": "Выведи всех сотрудников, кроме тех, кто одновременно из <code>'Paris'</code> и в <code>'HR'</code>. Используй <code>NOT ( … AND … )</code>."},
                 "answer": "SELECT * FROM employees\nWHERE NOT (city = 'Paris' AND department = 'HR');"},
                {"id": "2.d3",
                 "text": {"en": "The same as the previous task, but without brackets: rewrite it with De Morgan's law and <code>&lt;&gt;</code>.", "ru": "То же, что в прошлом задании, но без скобок: перепиши по закону де Моргана через <code>&lt;&gt;</code>."},
                 "answer": "SELECT * FROM employees\nWHERE city <> 'Paris' OR department <> 'HR';"},
                {"id": "2.d4",
                 "text": {"en": "Get all employees who were hired neither before 2016 nor after 2020. Start from <code>NOT (hire_year &lt; 2016 OR hire_year &gt; 2020)</code> and write it without <code>NOT</code>.", "ru": "Выведи всех сотрудников, которых наняли не раньше 2016 и не позже 2020 года. Начни с <code>NOT (hire_year &lt; 2016 OR hire_year &gt; 2020)</code> и запиши без <code>NOT</code>."},
                 "answer": "SELECT * FROM employees\nWHERE hire_year >= 2016 AND hire_year <= 2020;"},
                # Section C
                {"id": "2.15", "section": {"en": "C · BETWEEN", "ru": "C · BETWEEN"},
                 "intro": {
                     "en": '''<p><code>x BETWEEN a AND b</code> is a short way to write <code>x &gt;= a AND x &lt;= b</code>. Both ends are <b>included</b>.</p>
<p><b>Example:</b> employees with a bonus from 3000 to 6000.</p>''',
                     "ru": '''<p><code>x BETWEEN a AND b</code> — короткая запись для <code>x &gt;= a AND x &lt;= b</code>. Обе границы <b>включаются</b>.</p>
<p><b>Пример:</b> сотрудники с бонусом от 3000 до 6000.</p>''',
                 },
                 "example": "SELECT first_name, bonus\nFROM employees\nWHERE bonus BETWEEN 3000 AND 6000;",
                 "text": {"en": "Get all employees with salary between 45000 and 65000 (inclusive).", "ru": "Выведи всех сотрудников с зарплатой от 45000 до 65000 включительно."},
                 "answer": "SELECT * FROM employees WHERE salary BETWEEN 45000 AND 65000;"},
                {"id": "2.16", "text": {"en": "Get all products with price between 20 and 200.", "ru": "Выведи все товары с ценой от 20 до 200."},
                 "answer": "SELECT * FROM products WHERE price BETWEEN 20 AND 200;"},
                {"id": "2.17", "text": {"en": "Get all employees hired between 2016 and 2019.", "ru": "Выведи всех сотрудников, нанятых с 2016 по 2019 год."},
                 "answer": "SELECT * FROM employees WHERE hire_year BETWEEN 2016 AND 2019;"},
                {"id": "2.18", "text": {"en": "Get all products with stock between 50 and 200.", "ru": "Выведи все товары, у которых <code>stock</code> от 50 до 200."},
                 "answer": "SELECT * FROM products WHERE stock BETWEEN 50 AND 200;"},
                # Section D
                {"id": "2.19", "section": {"en": "D · IN", "ru": "D · IN"},
                 "intro": {
                     "en": '''<p><code>x IN (a, b, c)</code> is true when <code>x</code> equals any value in the list. It replaces a chain of <code>OR</code>s: <code>x = a OR x = b OR x = c</code>.</p>
<p><b>Example:</b> employees hired in 2014, 2015 or 2022.</p>''',
                     "ru": '''<p><code>x IN (a, b, c)</code> верно, если <code>x</code> равен любому значению из списка. Это замена цепочки <code>OR</code>: <code>x = a OR x = b OR x = c</code>.</p>
<p><b>Пример:</b> сотрудники, нанятые в 2014, 2015 или 2022 году.</p>''',
                 },
                 "example": "SELECT first_name, hire_year\nFROM employees\nWHERE hire_year IN (2014, 2015, 2022);",
                 "text": {"en": "Get all employees who work in <code>'IT'</code> or <code>'Sales'</code> (use <code>IN</code>).", "ru": "Выведи всех сотрудников отделов <code>'IT'</code> и <code>'Sales'</code> (используй <code>IN</code>)."},
                 "answer": "SELECT * FROM employees WHERE department IN ('IT', 'Sales');"},
                {"id": "2.20", "text": {"en": "Get all products from suppliers <code>'TechCorp'</code> or <code>'PaperWorld'</code>.", "ru": "Выведи все товары поставщиков <code>'TechCorp'</code> и <code>'PaperWorld'</code>."},
                 "answer": "SELECT * FROM products WHERE supplier IN ('TechCorp', 'PaperWorld');"},
                {"id": "2.21", "text": {"en": "Get all employees from the cities <code>'London'</code>, <code>'Berlin'</code>, <code>'Madrid'</code>.", "ru": "Выведи всех сотрудников из городов <code>'London'</code>, <code>'Berlin'</code>, <code>'Madrid'</code>."},
                 "answer": "SELECT * FROM employees WHERE city IN ('London', 'Berlin', 'Madrid');"},
                {"id": "2.22", "text": {"en": "Get all products in the categories <code>'Electronics'</code> or <code>'Furniture'</code>.", "ru": "Выведи все товары категорий <code>'Electronics'</code> и <code>'Furniture'</code>."},
                 "answer": "SELECT * FROM products WHERE category IN ('Electronics', 'Furniture');"},
                # Section E
                {"id": "2.23", "section": {"en": "E · LIKE", "ru": "E · LIKE"},
                 "intro": {
                     "en": '''<p><code>LIKE</code> compares text with a pattern. <code>%</code> means any number of characters (even none), <code>_</code> means exactly one character. <code>'A%'</code> starts with A, <code>'%a'</code> ends with a, <code>'%a%'</code> contains a.</p>
<p><b>Example:</b> employees whose last name ends with "r".</p>''',
                     "ru": '''<p><code>LIKE</code> сравнивает текст с шаблоном. <code>%</code> — любое количество символов (даже ноль), <code>_</code> — ровно один символ. <code>'A%'</code> начинается на A, <code>'%a'</code> заканчивается на a, <code>'%a%'</code> содержит a.</p>
<p><b>Пример:</b> сотрудники, чья фамилия заканчивается на «r».</p>''',
                 },
                 "example": "SELECT first_name, last_name\nFROM employees\nWHERE last_name LIKE '%r';",
                 "text": {"en": "Get all employees whose first name starts with <code>'A'</code>.", "ru": "Выведи всех сотрудников, чьё имя начинается на <code>'A'</code>."},
                 "answer": "SELECT * FROM employees WHERE first_name LIKE 'A%';"},
                {"id": "2.24", "text": {"en": "Get all products whose name ends with <code>'e'</code>.", "ru": "Выведи все товары, название которых заканчивается на <code>'e'</code>."},
                 "answer": "SELECT * FROM products WHERE product_name LIKE '%e';"},
                {"id": "2.25", "text": {"en": "Get all employees whose last name contains <code>'son'</code>.", "ru": "Выведи всех сотрудников, в фамилии которых есть <code>'son'</code>."},
                 "answer": "SELECT * FROM employees WHERE last_name LIKE '%son%';"},
                {"id": "2.26", "text": {"en": "Get all products whose name contains the word <code>'Set'</code>.", "ru": "Выведи все товары, в названии которых есть слово <code>'Set'</code>."},
                 "answer": "SELECT * FROM products WHERE product_name LIKE '%Set%';"},
                {"id": "2.27", "text": {"en": "Get all employees whose first name has exactly 5 letters (use <code>_</code>).", "ru": "Выведи всех сотрудников, чьё имя состоит ровно из 5 букв (используй <code>_</code>)."},
                 "answer": "SELECT * FROM employees WHERE first_name LIKE '_____';"},
                {"id": "2.28", "text": {"en": "Get all products whose name starts with <code>'B'</code>.", "ru": "Выведи все товары, название которых начинается на <code>'B'</code>."},
                 "answer": "SELECT * FROM products WHERE product_name LIKE 'B%';"},
                # Section F
                {"id": "2.29", "section": {"en": "F · NULL", "ru": "F · NULL"},
                 "intro": {
                     "en": '''<p><code>NULL</code> means "no value", like an empty cell. Any comparison with <code>NULL</code>, even <code>= NULL</code>, is never true, so <code>WHERE bonus = NULL</code> returns nothing. Use <code>IS NULL</code> and <code>IS NOT NULL</code>.</p>
<p><b>Example:</b> employees in Paris who have no bonus.</p>''',
                     "ru": '''<p><code>NULL</code> значит «значения нет», как пустая клетка. Любое сравнение с <code>NULL</code>, даже <code>= NULL</code>, никогда не верно, поэтому <code>WHERE bonus = NULL</code> ничего не вернёт. Используй <code>IS NULL</code> и <code>IS NOT NULL</code>.</p>
<p><b>Пример:</b> сотрудники из Парижа без бонуса.</p>''',
                 },
                 "example": "SELECT first_name, city, bonus\nFROM employees\nWHERE city = 'Paris' AND bonus IS NULL;",
                 "text": {"en": "Get all employees who have a bonus (<code>bonus IS NOT NULL</code>).", "ru": "Выведи всех сотрудников, у которых есть бонус (<code>bonus IS NOT NULL</code>)."},
                 "answer": "SELECT * FROM employees WHERE bonus IS NOT NULL;"},
                {"id": "2.30", "text": {"en": "Get all employees who do NOT have a bonus.", "ru": "Выведи всех сотрудников, у которых НЕТ бонуса."},
                 "answer": "SELECT * FROM employees WHERE bonus IS NULL;"},
                {"id": "2.31", "text": {"en": "Get all employees who have a bonus greater than 4000.", "ru": "Выведи всех сотрудников с бонусом больше 4000."},
                 "answer": "SELECT * FROM employees WHERE bonus > 4000;"},
                # Section G
                {"id": "2.32", "section": {"en": "G · DISTINCT", "ru": "G · DISTINCT"},
                 "intro": {
                     "en": '''<p><code>SELECT DISTINCT</code> removes duplicate rows from the result, like "Remove duplicates" in Excel. With several columns, a row is a duplicate only if <b>all</b> its selected values repeat. <code>DISTINCT</code> goes right after <code>SELECT</code> and works together with <code>WHERE</code>.</p>
<p><b>Example:</b> the years in which people were hired. There are 10 employees but only 9 different years, because 2018 appears twice.</p>''',
                     "ru": '''<p><code>SELECT DISTINCT</code> убирает из результата повторяющиеся строки, как «Удалить дубликаты» в Excel. Если столбцов несколько, строка считается повтором, только когда повторяются <b>все</b> выбранные значения. <code>DISTINCT</code> пишется сразу после <code>SELECT</code> и работает вместе с <code>WHERE</code>.</p>
<p><b>Пример:</b> годы, в которые нанимали сотрудников. Сотрудников 10, а разных лет 9: 2018 встречается дважды.</p>''',
                 },
                 "example": "SELECT DISTINCT hire_year\nFROM employees;",
                 "text": {"en": "List every department once, without duplicates.", "ru": "Выведи список отделов, каждый по одному разу."},
                 "answer": "SELECT DISTINCT department FROM employees;"},
                {"id": "2.33", "text": {"en": "List every city where employees work, without repeats.", "ru": "Выведи все города, где работают сотрудники, без повторов."},
                 "answer": "SELECT DISTINCT city FROM employees;"},
                {"id": "2.34", "text": {"en": "List all suppliers of products, each one once.", "ru": "Выведи всех поставщиков товаров, каждого по одному разу."},
                 "answer": "SELECT DISTINCT supplier FROM products;"},
                {"id": "2.35", "text": {"en": "List every unique combination of <code>department</code> and <code>city</code>.", "ru": "Выведи все уникальные сочетания <code>department</code> и <code>city</code>."},
                 "answer": "SELECT DISTINCT department, city FROM employees;"},
                {"id": "2.36", "text": {"en": "List the cities that have at least one employee with salary above 50000, without repeats.", "ru": "Выведи без повторов города, где есть сотрудники с зарплатой выше 50000."},
                 "answer": "SELECT DISTINCT city FROM employees WHERE salary > 50000;"},
                {"id": "2.37", "text": {"en": "List the product categories that have products cheaper than 100, each category once.", "ru": "Выведи категории, в которых есть товары дешевле 100, каждую по одному разу."},
                 "answer": "SELECT DISTINCT category FROM products WHERE price < 100;"},
                # Section H
                {"id": "2.38", "section": {"en": "H · Mixed", "ru": "H · Всё вместе"},
                 "intro": {
                     "en": '''<p>Real questions combine everything above. Build the condition step by step: write one part, run it, check the rows, then add the next part with <code>AND</code> or <code>OR</code>.</p>
<p><b>Example:</b> IT employees in London or Madrid who have a bonus.</p>''',
                     "ru": '''<p>Настоящие задачи сочетают всё сразу. Собирай условие по шагам: напиши одну часть, запусти, проверь строки, потом добавь следующую через <code>AND</code> или <code>OR</code>.</p>
<p><b>Пример:</b> сотрудники IT из Лондона или Мадрида, у которых есть бонус.</p>''',
                 },
                 "example": "SELECT first_name, city, bonus\nFROM employees\nWHERE department = 'IT'\n  AND city IN ('London', 'Madrid')\n  AND bonus IS NOT NULL;",
                 "text": {"en": "Get all IT or Sales employees from <code>'London'</code> with salary &gt; 55000.", "ru": "Выведи всех сотрудников IT или Sales из <code>'London'</code> с зарплатой &gt; 55000."},
                 "answer": "SELECT * FROM employees\nWHERE department IN ('IT', 'Sales')\n  AND city = 'London'\n  AND salary > 55000;"},
                {"id": "2.39", "text": {"en": "Get all products in <code>'Electronics'</code> with price <code>BETWEEN</code> 50 <code>AND</code> 400 and stock &gt; 20.", "ru": "Выведи все товары <code>'Electronics'</code> с ценой <code>BETWEEN</code> 50 <code>AND</code> 400 и <code>stock</code> &gt; 20."},
                 "answer": "SELECT * FROM products\nWHERE category = 'Electronics'\n  AND price BETWEEN 50 AND 400\n  AND stock > 20;"},
                {"id": "2.40", "text": {"en": "Get all employees whose first name starts with <code>'J'</code> OR last name starts with <code>'B'</code>.", "ru": "Выведи всех сотрудников, у которых имя начинается на <code>'J'</code> ИЛИ фамилия на <code>'B'</code>."},
                 "answer": "SELECT * FROM employees\nWHERE first_name LIKE 'J%' OR last_name LIKE 'B%';"},
                {"id": "2.41", "text": {"en": "Get all products whose name contains <code>'o'</code> and whose category is NOT <code>'Furniture'</code>.", "ru": "Выведи все товары, в названии которых есть <code>'o'</code>, а категория НЕ <code>'Furniture'</code>."},
                 "answer": "SELECT * FROM products\nWHERE product_name LIKE '%o%' AND category <> 'Furniture';"},
                # ---- Extra practice: optional, counted separately from the main tasks ----
                {"id": "2.x1",
                 "extra": True,
                 "section": {"en": "Extra · Comparison operators", "ru": "Доп. · Операторы сравнения"},
                 "text": {"en": "Get all employees with salary less than 50000.", "ru": "Выведи всех сотрудников с зарплатой меньше 50000."},
                 "answer": "SELECT * FROM employees WHERE salary < 50000;"},
                {"id": "2.x2",
                 "extra": True,
                 "text": {"en": "Get all products with price greater than 100.", "ru": "Выведи все товары дороже 100."},
                 "answer": "SELECT * FROM products WHERE price > 100;"},
                {"id": "2.x3",
                 "extra": True,
                 "text": {"en": "Get all employees hired after 2018.", "ru": "Выведи всех сотрудников, нанятых после 2018 года."},
                 "answer": "SELECT * FROM employees WHERE hire_year > 2018;"},
                {"id": "2.x4",
                 "extra": True,
                 "text": {"en": "Get all products with <code>stock</code> greater than 100.", "ru": "Выведи все товары, у которых <code>stock</code> больше 100."},
                 "answer": "SELECT * FROM products WHERE stock > 100;"},
                {"id": "2.x5",
                 "extra": True,
                 "text": {"en": "Get all employees whose bonus is less than 5000.", "ru": "Выведи всех сотрудников с бонусом меньше 5000."},
                 "answer": "SELECT * FROM employees WHERE bonus < 5000;"},
                {"id": "2.x6",
                 "extra": True,
                 "text": {"en": "Get all products with <code>product_id</code> greater than 5.", "ru": "Выведи все товары с <code>product_id</code> больше 5."},
                 "answer": "SELECT * FROM products WHERE product_id > 5;"},
                {"id": "2.x7",
                 "extra": True,
                 "text": {"en": "Get all employees whose last name is exactly <code>'Smith'</code>.", "ru": "Выведи всех сотрудников с фамилией ровно <code>'Smith'</code>."},
                 "answer": "SELECT * FROM employees WHERE last_name = 'Smith';"},
                {"id": "2.x8",
                 "extra": True,
                 "text": {"en": "Get all products whose category is exactly <code>'Furniture'</code>.", "ru": "Выведи все товары категории ровно <code>'Furniture'</code>."},
                 "answer": "SELECT * FROM products WHERE category = 'Furniture';"},
                {"id": "2.x9",
                 "extra": True,
                 "section": {"en": "Extra · AND / OR / NOT", "ru": "Доп. · AND / OR / NOT"},
                 "intro": {"en": '''<p>New here: <code>NOT</code> in front of a group in parentheses. <code>NOT (A OR B)</code> means "neither A nor B", and it is the same as <code>NOT A AND NOT B</code>. This rule is called De Morgan's law. Another way to write it is <code>NOT IN</code>: <code>supplier NOT IN ('TechCorp', 'GadgetInc')</code>.</p>
<p><b>Example:</b> products that come from neither TechCorp nor GadgetInc.</p>''', "ru": '''<p>Новое здесь: <code>NOT</code> перед группой в скобках. <code>NOT (A OR B)</code> значит «ни A, ни B», и это то же самое, что <code>NOT A AND NOT B</code>. Это правило называется законом де Моргана. Ещё один способ записи — <code>NOT IN</code>: <code>supplier NOT IN ('TechCorp', 'GadgetInc')</code>.</p>
<p><b>Пример:</b> товары, которые поставляет не TechCorp и не GadgetInc.</p>'''},
                 "example": "SELECT product_name, supplier\nFROM products\nWHERE NOT (supplier = 'TechCorp' OR supplier = 'GadgetInc');",
                 "text": {"en": "Get all employees in the <code>'Sales'</code> department from <code>'London'</code>.", "ru": "Выведи всех сотрудников отдела <code>'Sales'</code> из <code>'London'</code>."},
                 "answer": "SELECT * FROM employees WHERE department = 'Sales' AND city = 'London';"},
                {"id": "2.x10",
                 "extra": True,
                 "text": {"en": "Get all products in <code>'Stationery'</code> with price less than 10.", "ru": "Выведи все товары <code>'Stationery'</code> дешевле 10."},
                 "answer": "SELECT * FROM products WHERE category = 'Stationery' AND price < 10;"},
                {"id": "2.x11",
                 "extra": True,
                 "text": {"en": "Get all employees from <code>'London'</code> OR <code>'Madrid'</code>.", "ru": "Выведи всех сотрудников из <code>'London'</code> ИЛИ <code>'Madrid'</code>."},
                 "answer": "SELECT * FROM employees WHERE city = 'London' OR city = 'Madrid';"},
                {"id": "2.x12",
                 "extra": True,
                 "text": {"en": "Get all products from <code>'BrightHome'</code> OR <code>'PaperWorld'</code>.", "ru": "Выведи все товары от <code>'BrightHome'</code> ИЛИ <code>'PaperWorld'</code>."},
                 "answer": "SELECT * FROM products WHERE supplier = 'BrightHome' OR supplier = 'PaperWorld';"},
                {"id": "2.x13",
                 "extra": True,
                 "text": {"en": "Get all employees from <code>'Paris'</code> OR <code>'Berlin'</code> with salary above 50000.", "ru": "Выведи всех сотрудников из <code>'Paris'</code> ИЛИ <code>'Berlin'</code> с зарплатой выше 50000."},
                 "answer": "SELECT * FROM employees\nWHERE (city = 'Paris' OR city = 'Berlin') AND salary > 50000;"},
                {"id": "2.x14",
                 "extra": True,
                 "text": {"en": "Get all products NOT in <code>'Electronics'</code> with price greater than 50.", "ru": "Выведи все товары НЕ из <code>'Electronics'</code> дороже 50."},
                 "answer": "SELECT * FROM products WHERE NOT category = 'Electronics' AND price > 50;"},
                {"id": "2.x15",
                 "extra": True,
                 "text": {"en": "Get all employees who are NOT from <code>'London'</code> and NOT from <code>'Paris'</code>.", "ru": "Выведи всех сотрудников НЕ из <code>'London'</code> и НЕ из <code>'Paris'</code>."},
                 "answer": "SELECT * FROM employees WHERE city <> 'London' AND city <> 'Paris';"},
                {"id": "2.x16",
                 "extra": True,
                 "text": {"en": "Get all employees who are NOT in <code>'HR'</code> or <code>'Sales'</code>. Write it as <code>NOT (… OR …)</code>.", "ru": "Выведи всех сотрудников, которые НЕ в <code>'HR'</code> и не в <code>'Sales'</code>. Запиши через <code>NOT (… OR …)</code>."},
                 "answer": "SELECT * FROM employees WHERE NOT (department = 'HR' OR department = 'Sales');"},
                {"id": "2.x17",
                 "extra": True,
                 "text": {"en": "Get all products that are NOT in <code>'Furniture'</code> or <code>'Stationery'</code>. Write it as <code>NOT (… OR …)</code>.", "ru": "Выведи все товары, которые НЕ из <code>'Furniture'</code> и не из <code>'Stationery'</code>. Запиши через <code>NOT (… OR …)</code>."},
                 "answer": "SELECT * FROM products WHERE NOT (category = 'Furniture' OR category = 'Stationery');"},
                {"id": "2.x18",
                 "extra": True,
                 "section": {"en": "Extra · BETWEEN", "ru": "Доп. · BETWEEN"},
                 "text": {"en": "Get all employees with bonus between 3000 and 6000.", "ru": "Выведи всех сотрудников с бонусом от 3000 до 6000."},
                 "answer": "SELECT * FROM employees WHERE bonus BETWEEN 3000 AND 6000;"},
                {"id": "2.x19",
                 "extra": True,
                 "text": {"en": "Get all products with price between 10 and 100.", "ru": "Выведи все товары с ценой от 10 до 100."},
                 "answer": "SELECT * FROM products WHERE price BETWEEN 10 AND 100;"},
                {"id": "2.x20",
                 "extra": True,
                 "text": {"en": "Get all employees hired between 2018 and 2021.", "ru": "Выведи всех сотрудников, нанятых с 2018 по 2021 год."},
                 "answer": "SELECT * FROM employees WHERE hire_year BETWEEN 2018 AND 2021;"},
                {"id": "2.x21",
                 "extra": True,
                 "text": {"en": "Get all products with <code>product_id</code> between 3 and 7.", "ru": "Выведи все товары с <code>product_id</code> от 3 до 7."},
                 "answer": "SELECT * FROM products WHERE product_id BETWEEN 3 AND 7;"},
                {"id": "2.x22",
                 "extra": True,
                 "text": {"en": "Get all employees with salary between 40000 and 50000.", "ru": "Выведи всех сотрудников с зарплатой от 40000 до 50000."},
                 "answer": "SELECT * FROM employees WHERE salary BETWEEN 40000 AND 50000;"},
                {"id": "2.x23",
                 "extra": True,
                 "text": {"en": "Get all products with <code>stock</code> between 100 and 300.", "ru": "Выведи все товары, у которых <code>stock</code> от 100 до 300."},
                 "answer": "SELECT * FROM products WHERE stock BETWEEN 100 AND 300;"},
                {"id": "2.x24",
                 "extra": True,
                 "section": {"en": "Extra · IN", "ru": "Доп. · IN"},
                 "text": {"en": "Get all employees in the departments <code>'IT'</code> or <code>'HR'</code> (use <code>IN</code>).", "ru": "Выведи всех сотрудников отделов <code>'IT'</code> и <code>'HR'</code> (используй <code>IN</code>)."},
                 "answer": "SELECT * FROM employees WHERE department IN ('IT', 'HR');"},
                {"id": "2.x25",
                 "extra": True,
                 "text": {"en": "Get the products with odd ids: <code>product_id</code> 1, 3, 5, 7, 9.", "ru": "Выведи товары с нечётными id: <code>product_id</code> 1, 3, 5, 7, 9."},
                 "answer": "SELECT * FROM products WHERE product_id IN (1, 3, 5, 7, 9);"},
                {"id": "2.x26",
                 "extra": True,
                 "text": {"en": "Get all employees from the cities <code>'Paris'</code> or <code>'Madrid'</code>.", "ru": "Выведи всех сотрудников из городов <code>'Paris'</code> и <code>'Madrid'</code>."},
                 "answer": "SELECT * FROM employees WHERE city IN ('Paris', 'Madrid');"},
                {"id": "2.x27",
                 "extra": True,
                 "text": {"en": "Get all products from the suppliers <code>'GadgetInc'</code> or <code>'BrightHome'</code>.", "ru": "Выведи все товары поставщиков <code>'GadgetInc'</code> и <code>'BrightHome'</code>."},
                 "answer": "SELECT * FROM products WHERE supplier IN ('GadgetInc', 'BrightHome');"},
                {"id": "2.x28",
                 "extra": True,
                 "text": {"en": "Get all employees whose last name is <code>'Brown'</code>, <code>'Miller'</code> or <code>'Taylor'</code>.", "ru": "Выведи всех сотрудников с фамилией <code>'Brown'</code>, <code>'Miller'</code> или <code>'Taylor'</code>."},
                 "answer": "SELECT * FROM employees WHERE last_name IN ('Brown', 'Miller', 'Taylor');"},
                {"id": "2.x29",
                 "extra": True,
                 "text": {"en": "Get all products in the categories <code>'Electronics'</code> or <code>'Stationery'</code>.", "ru": "Выведи все товары категорий <code>'Electronics'</code> и <code>'Stationery'</code>."},
                 "answer": "SELECT * FROM products WHERE category IN ('Electronics', 'Stationery');"},
                {"id": "2.x30",
                 "extra": True,
                 "section": {"en": "Extra · LIKE", "ru": "Доп. · LIKE"},
                 "text": {"en": "Get all employees whose first name ends with <code>'a'</code>.", "ru": "Выведи всех сотрудников, чьё имя заканчивается на <code>'a'</code>."},
                 "answer": "SELECT * FROM employees WHERE first_name LIKE '%a';"},
                {"id": "2.x31",
                 "extra": True,
                 "text": {"en": "Get all products whose name starts with <code>'W'</code>.", "ru": "Выведи все товары, название которых начинается на <code>'W'</code>."},
                 "answer": "SELECT * FROM products WHERE product_name LIKE 'W%';"},
                {"id": "2.x32",
                 "extra": True,
                 "text": {"en": "Get all employees whose last name contains <code>'er'</code>.", "ru": "Выведи всех сотрудников, в фамилии которых есть <code>'er'</code>."},
                 "answer": "SELECT * FROM employees WHERE last_name LIKE '%er%';"},
                {"id": "2.x33",
                 "extra": True,
                 "text": {"en": "Get all products whose name contains <code>'o'</code> anywhere.", "ru": "Выведи все товары, в названии которых где угодно есть <code>'o'</code>."},
                 "answer": "SELECT * FROM products WHERE product_name LIKE '%o%';"},
                {"id": "2.x34",
                 "extra": True,
                 "text": {"en": "Get all employees whose first name has exactly 4 letters (use <code>_</code>).", "ru": "Выведи всех сотрудников, чьё имя ровно из 4 букв (используй <code>_</code>)."},
                 "answer": "SELECT * FROM employees WHERE first_name LIKE '____';"},
                {"id": "2.x35",
                 "extra": True,
                 "text": {"en": "Get all employees whose first name has exactly 3 letters.", "ru": "Выведи всех сотрудников, чьё имя ровно из 3 букв."},
                 "answer": "SELECT * FROM employees WHERE first_name LIKE '___';"},
                {"id": "2.x36",
                 "extra": True,
                 "text": {"en": "Get all employees whose last name starts with <code>'M'</code> and ends with <code>'e'</code>.", "ru": "Выведи всех сотрудников, чья фамилия начинается на <code>'M'</code> и заканчивается на <code>'e'</code>."},
                 "answer": "SELECT * FROM employees WHERE last_name LIKE 'M%e';"},
                {"id": "2.x37",
                 "extra": True,
                 "text": {"en": "Get all products whose name starts with <code>'L'</code> and contains <code>'o'</code>.", "ru": "Выведи все товары, название которых начинается на <code>'L'</code> и содержит <code>'o'</code>."},
                 "answer": "SELECT * FROM products WHERE product_name LIKE 'L%o%';"},
                {"id": "2.x38",
                 "extra": True,
                 "text": {"en": "Get all employees whose first name contains <code>'i'</code> anywhere.", "ru": "Выведи всех сотрудников, в имени которых где угодно есть <code>'i'</code>."},
                 "answer": "SELECT * FROM employees WHERE first_name LIKE '%i%';"},
                {"id": "2.x39",
                 "extra": True,
                 "text": {"en": "Get all products whose name ends with <code>'r'</code>.", "ru": "Выведи все товары, название которых заканчивается на <code>'r'</code>."},
                 "answer": "SELECT * FROM products WHERE product_name LIKE '%r';"},
                {"id": "2.x40",
                 "extra": True,
                 "section": {"en": "Extra · NULL", "ru": "Доп. · NULL"},
                 "text": {"en": "Show <code>first_name</code>, <code>department</code> and <code>bonus</code> of the employees who have no bonus.", "ru": "Покажи <code>first_name</code>, <code>department</code> и <code>bonus</code> сотрудников без бонуса."},
                 "answer": "SELECT first_name, department, bonus FROM employees WHERE bonus IS NULL;"},
                {"id": "2.x41",
                 "extra": True,
                 "text": {"en": "Get all employees who have a bonus and earn more than 50000.", "ru": "Выведи всех сотрудников, у которых есть бонус и зарплата больше 50000."},
                 "answer": "SELECT * FROM employees WHERE bonus IS NOT NULL AND salary > 50000;"},
                {"id": "2.x42",
                 "extra": True,
                 "text": {"en": "Get all IT employees who have no bonus.", "ru": "Выведи всех сотрудников IT без бонуса."},
                 "answer": "SELECT * FROM employees WHERE bonus IS NULL AND department = 'IT';"},
                {"id": "2.x43",
                 "extra": True,
                 "text": {"en": "Get all employees whose bonus is missing OR below 4000.", "ru": "Выведи всех сотрудников, у которых бонуса нет ИЛИ он меньше 4000."},
                 "answer": "SELECT * FROM employees WHERE bonus IS NULL OR bonus < 4000;"},
                {"id": "2.x44",
                 "extra": True,
                 "section": {"en": "Extra · Mixed challenge", "ru": "Доп. · Всё вместе"},
                 "intro": {"en": '''<p>One new piece: <code>NOT BETWEEN a AND b</code> keeps the values <b>outside</b> the range, below <code>a</code> or above <code>b</code>. The rest is everything you already know, three or four conditions at once.</p>
<p><b>Example:</b> products that cost less than 10 or more than 200.</p>''', "ru": '''<p>Одна новая деталь: <code>NOT BETWEEN a AND b</code> оставляет значения <b>вне</b> диапазона — меньше <code>a</code> или больше <code>b</code>. Остальное ты уже знаешь, просто по три-четыре условия сразу.</p>
<p><b>Пример:</b> товары дешевле 10 или дороже 200.</p>'''},
                 "example": "SELECT product_name, price\nFROM products\nWHERE price NOT BETWEEN 10 AND 200;",
                 "text": {"en": "Get all IT employees from <code>'London'</code> with salary <code>BETWEEN</code> 55000 <code>AND</code> 80000.", "ru": "Выведи всех сотрудников IT из <code>'London'</code> с зарплатой <code>BETWEEN</code> 55000 <code>AND</code> 80000."},
                 "answer": "SELECT * FROM employees\nWHERE department = 'IT'\n  AND city = 'London'\n  AND salary BETWEEN 55000 AND 80000;"},
                {"id": "2.x45",
                 "extra": True,
                 "text": {"en": "Get all <code>'Electronics'</code> products from <code>'TechCorp'</code> with price greater than 300.", "ru": "Выведи все товары <code>'Electronics'</code> от <code>'TechCorp'</code> дороже 300."},
                 "answer": "SELECT * FROM products\nWHERE category = 'Electronics'\n  AND supplier = 'TechCorp'\n  AND price > 300;"},
                {"id": "2.x46",
                 "extra": True,
                 "text": {"en": "Get all Sales or HR employees who are NOT from <code>'Paris'</code> and have a bonus.", "ru": "Выведи всех сотрудников Sales или HR, которые НЕ из <code>'Paris'</code> и у которых есть бонус."},
                 "answer": "SELECT * FROM employees\nWHERE department IN ('Sales', 'HR')\n  AND city <> 'Paris'\n  AND bonus IS NOT NULL;"},
                {"id": "2.x47",
                 "extra": True,
                 "text": {"en": "Get all <code>'PaperWorld'</code> products whose name contains <code>'e'</code> and price is less than 15.", "ru": "Выведи все товары <code>'PaperWorld'</code>, в названии которых есть <code>'e'</code>, дешевле 15."},
                 "answer": "SELECT * FROM products\nWHERE supplier = 'PaperWorld'\n  AND product_name LIKE '%e%'\n  AND price < 15;"},
                {"id": "2.x48",
                 "extra": True,
                 "text": {"en": "Get all employees whose first name starts with <code>'A'</code> OR last name starts with <code>'J'</code>, and whose salary is above 55000.", "ru": "Выведи всех сотрудников, у которых имя начинается на <code>'A'</code> ИЛИ фамилия на <code>'J'</code>, а зарплата выше 55000."},
                 "answer": "SELECT * FROM employees\nWHERE (first_name LIKE 'A%' OR last_name LIKE 'J%')\n  AND salary > 55000;"},
                {"id": "2.x49",
                 "extra": True,
                 "text": {"en": "Get all products NOT in <code>'Furniture'</code> with <code>stock</code> between 100 and 500 and supplier NOT <code>'BrightHome'</code>.", "ru": "Выведи все товары НЕ из <code>'Furniture'</code>, у которых <code>stock</code> от 100 до 500, а поставщик НЕ <code>'BrightHome'</code>."},
                 "answer": "SELECT * FROM products\nWHERE category <> 'Furniture'\n  AND stock BETWEEN 100 AND 500\n  AND supplier <> 'BrightHome';"},
                {"id": "2.x50",
                 "extra": True,
                 "text": {"en": "Get all employees hired between 2015 and 2019, NOT in <code>'HR'</code>, with salary <code>NOT BETWEEN</code> 45000 <code>AND</code> 50000.", "ru": "Выведи всех сотрудников, нанятых с 2015 по 2019 год, НЕ из <code>'HR'</code>, с зарплатой <code>NOT BETWEEN</code> 45000 <code>AND</code> 50000."},
                 "answer": "SELECT * FROM employees\nWHERE hire_year BETWEEN 2015 AND 2019\n  AND department <> 'HR'\n  AND salary NOT BETWEEN 45000 AND 50000;"},
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
