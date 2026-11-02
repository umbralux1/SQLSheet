"""
SQL course content.

Everything here is served to the browser by /course.js EXCEPT the task answers,
which stay on the server: /api/check compares a student's result with the
answer's result, and /api/answers/<id> shows them to the logged-in teacher.

To add a lesson: fill in theory / seed / tables / tasks (every task needs an
"answer" query) and set "available": True.
"""

# The online shop of the "SQL for Analytics" track. Every lesson of the track uses it;
# /course.js sends it once ("seeds") and the lessons point to it with "seed_ref".
SHOP_SEED = """CREATE TABLE customers (
    customer_id  INTEGER PRIMARY KEY,
    name         TEXT,
    city         TEXT,
    signup_date  DATE,
    channel      TEXT
);
INSERT INTO customers VALUES
(1, 'Anna', 'Madrid', '2024-08-24', 'social'),
(2, 'Ben', 'Berlin', '2024-06-01', 'social'),
(3, 'Clara', 'London', '2025-01-24', 'organic'),
(4, 'David', 'London', '2024-09-09', 'organic'),
(5, 'Elena', 'Madrid', '2025-01-03', 'organic'),
(6, 'Felix', 'Rome', '2024-07-21', 'organic'),
(7, 'Grace', NULL, '2024-08-08', 'referral'),
(8, 'Hugo', 'Paris', '2024-12-16', 'organic'),
(9, 'Iris', 'Madrid', '2025-01-20', 'social'),
(10, 'Jack', 'Rome', '2025-05-29', 'social'),
(11, 'Kate', 'Rome', '2024-09-22', 'organic'),
(12, 'Leo', 'Paris', '2024-10-03', 'ads'),
(13, 'Maria', 'Paris', '2024-09-27', 'ads'),
(14, 'Nick', 'London', '2025-06-12', 'social'),
(15, 'Olga', 'Berlin', '2025-09-15', 'ads'),
(16, 'Paul', 'Berlin', '2024-11-28', 'ads'),
(17, 'Quinn', 'Madrid', '2025-09-11', 'ads'),
(18, 'Rosa', 'Rome', '2025-08-16', 'organic'),
(19, 'Sam', NULL, '2025-05-06', 'social'),
(20, 'Tina', 'Berlin', '2025-02-06', 'organic'),
(21, 'Umar', 'Paris', '2025-04-16', 'social'),
(22, 'Vera', 'Berlin', '2025-05-06', 'organic'),
(23, 'Will', 'Berlin', '2024-10-29', 'ads'),
(24, 'Xenia', 'London', '2024-10-30', 'organic'),
(25, 'Yuri', 'Rome', '2024-11-05', 'social'),
(26, 'Zoe', 'Rome', '2025-05-18', 'organic'),
(27, 'Adam', 'Rome', '2024-06-26', 'social'),
(28, 'Bella', 'London', '2025-07-23', 'organic'),
(29, 'Chris', 'Paris', '2024-12-27', 'organic'),
(30, 'Dina', 'Rome', '2025-08-29', 'social'),
(31, 'Eric', 'Berlin', '2024-11-02', 'ads'),
(32, 'Fiona', 'Rome', '2024-09-05', 'ads'),
(33, 'Gleb', NULL, '2024-10-24', 'social'),
(34, 'Helen', 'Berlin', '2025-01-31', 'organic'),
(35, 'Ivan', 'Berlin', '2024-10-18', 'referral'),
(36, 'Julia', 'Madrid', '2024-11-02', 'social'),
(37, 'Karl', 'Rome', '2025-01-21', 'referral'),
(38, 'Lina', 'London', '2024-12-06', 'social'),
(39, 'Mark', 'Paris', '2024-11-04', 'ads'),
(40, 'Nina', 'Rome', '2025-04-19', 'ads');
CREATE TABLE products (
    product_id  INTEGER PRIMARY KEY,
    name        TEXT,
    category    TEXT,
    price       INTEGER,
    cost        INTEGER
);
INSERT INTO products VALUES
(1, 'Wireless Earbuds', 'Electronics', 89, 52),
(2, 'Smart Watch', 'Electronics', 249, 160),
(3, 'USB-C Charger', 'Electronics', 29, 11),
(4, 'Bluetooth Speaker', 'Electronics', 119, 70),
(5, 'Coffee Maker', 'Home', 139, 85),
(6, 'Desk Lamp', 'Home', 45, 22),
(7, 'Throw Blanket', 'Home', 39, 15),
(8, 'Ceramic Mug Set', 'Home', 25, 9),
(9, 'Mystery Novel', 'Books', 15, 6),
(10, 'Cookbook', 'Books', 32, 14),
(11, 'SQL for Beginners', 'Books', 41, 17),
(12, 'Yoga Mat', 'Sport', 35, 13),
(13, 'Running Shoes', 'Sport', 129, 74),
(14, 'Water Bottle', 'Sport', 19, 6);
CREATE TABLE orders (
    order_id     INTEGER PRIMARY KEY,
    customer_id  INTEGER,
    order_date   DATE,
    status       TEXT,
    promo_code   TEXT,
    amount       INTEGER
);
INSERT INTO orders VALUES
(1, 2, '2025-01-13', 'returned', NULL, 41),
(2, 16, '2025-01-16', 'delivered', 'WELCOME10', 125),
(3, 11, '2025-01-22', 'delivered', NULL, 296),
(4, 37, '2025-01-23', 'delivered', NULL, 87),
(5, 12, '2025-01-24', 'delivered', 'WELCOME10', 125),
(6, 8, '2025-02-17', 'delivered', 'WELCOME10', 26),
(7, 35, '2025-02-23', 'delivered', NULL, 79),
(8, 37, '2025-03-04', 'delivered', NULL, 15),
(9, 25, '2025-03-05', 'delivered', 'SPRING', 41),
(10, 9, '2025-03-09', 'delivered', 'SPRING', 35),
(11, 37, '2025-03-10', 'delivered', NULL, 129),
(12, 32, '2025-03-15', 'returned', NULL, 39),
(13, 27, '2025-03-25', 'delivered', NULL, 258),
(14, 35, '2025-04-17', 'delivered', NULL, 69),
(15, 37, '2025-04-21', 'delivered', NULL, 89),
(16, 32, '2025-04-24', 'delivered', NULL, 19),
(17, 25, '2025-04-25', 'delivered', NULL, 184),
(18, 40, '2025-05-06', 'delivered', 'SPRING', 107),
(19, 3, '2025-05-09', 'delivered', NULL, 45),
(20, 11, '2025-05-09', 'delivered', NULL, 30),
(21, 9, '2025-05-11', 'delivered', NULL, 39),
(22, 2, '2025-05-21', 'delivered', NULL, 80),
(23, 26, '2025-05-21', 'delivered', NULL, 58),
(24, 9, '2025-05-22', 'delivered', 'SPRING', 80),
(25, 12, '2025-05-22', 'delivered', NULL, 338),
(26, 37, '2025-05-25', 'delivered', NULL, 135),
(27, 8, '2025-05-26', 'delivered', 'SPRING', 35),
(28, 20, '2025-05-26', 'delivered', 'WELCOME10', 29),
(29, 9, '2025-06-03', 'delivered', NULL, 45),
(30, 14, '2025-06-12', 'delivered', 'WELCOME10', 116),
(31, 6, '2025-06-25', 'delivered', 'WELCOME10', 37),
(32, 8, '2025-07-03', 'delivered', NULL, 83),
(33, 36, '2025-07-04', 'delivered', 'WELCOME10', 26),
(34, 13, '2025-07-06', 'delivered', NULL, 187),
(35, 36, '2025-07-06', 'delivered', NULL, 45),
(36, 8, '2025-07-12', 'delivered', NULL, 41),
(37, 37, '2025-07-16', 'cancelled', NULL, 129),
(38, 9, '2025-07-18', 'delivered', NULL, 96),
(39, 24, '2025-07-21', 'delivered', 'WELCOME10', 26),
(40, 8, '2025-08-05', 'delivered', NULL, 119),
(41, 23, '2025-08-12', 'delivered', NULL, 25),
(42, 26, '2025-08-15', 'delivered', NULL, 32),
(43, 5, '2025-08-21', 'delivered', NULL, 128),
(44, 10, '2025-08-24', 'delivered', NULL, 32),
(45, 39, '2025-08-26', 'delivered', NULL, 258),
(46, 19, '2025-09-07', 'returned', NULL, 217),
(47, 20, '2025-09-10', 'delivered', NULL, 74),
(48, 31, '2025-09-11', 'delivered', NULL, 349),
(49, 2, '2025-09-14', 'delivered', NULL, 756),
(50, 26, '2025-09-16', 'delivered', NULL, 35),
(51, 37, '2025-09-16', 'delivered', NULL, 114),
(52, 3, '2025-09-22', 'delivered', NULL, 32),
(53, 6, '2025-09-27', 'returned', NULL, 25),
(54, 9, '2025-09-27', 'delivered', NULL, 523),
(55, 35, '2025-09-28', 'delivered', NULL, 87),
(56, 18, '2025-10-07', 'returned', 'WELCOME10', 224),
(57, 30, '2025-10-09', 'delivered', 'WELCOME10', 55),
(58, 20, '2025-10-10', 'returned', NULL, 19),
(59, 30, '2025-10-10', 'cancelled', NULL, 32),
(60, 11, '2025-10-11', 'delivered', NULL, 41),
(61, 29, '2025-10-11', 'delivered', NULL, 317),
(62, 32, '2025-10-11', 'delivered', NULL, 258),
(63, 8, '2025-10-13', 'delivered', NULL, 417),
(64, 37, '2025-10-14', 'delivered', NULL, 319),
(65, 31, '2025-10-18', 'cancelled', NULL, 29),
(66, 22, '2025-10-19', 'delivered', 'WELCOME10', 321),
(67, 8, '2025-10-27', 'returned', NULL, 134),
(68, 14, '2025-10-28', 'delivered', NULL, 29),
(69, 18, '2025-11-01', 'delivered', NULL, 154),
(70, 37, '2025-11-06', 'delivered', NULL, 376),
(71, 30, '2025-11-07', 'delivered', NULL, 89),
(72, 15, '2025-11-09', 'delivered', 'WELCOME10', 51),
(73, 18, '2025-11-09', 'delivered', NULL, 89),
(74, 3, '2025-11-10', 'delivered', NULL, 29),
(75, 9, '2025-11-10', 'delivered', NULL, 173),
(76, 31, '2025-11-12', 'delivered', NULL, 154),
(77, 27, '2025-11-15', 'returned', NULL, 15),
(78, 19, '2025-11-16', 'delivered', NULL, 212),
(79, 9, '2025-11-18', 'delivered', NULL, 29),
(80, 18, '2025-11-18', 'delivered', NULL, 29),
(81, 19, '2025-11-18', 'delivered', NULL, 19),
(82, 34, '2025-11-19', 'delivered', 'WELCOME10', 29),
(83, 28, '2025-11-21', 'delivered', 'WELCOME10', 150),
(84, 30, '2025-11-22', 'cancelled', NULL, 41),
(85, 8, '2025-11-23', 'delivered', NULL, 45),
(86, 9, '2025-11-25', 'delivered', 'BLACKFRIDAY', 197),
(87, 30, '2025-11-25', 'delivered', 'BLACKFRIDAY', 178),
(88, 35, '2025-11-26', 'delivered', 'BLACKFRIDAY', 288),
(89, 5, '2025-12-02', 'delivered', NULL, 293),
(90, 18, '2025-12-04', 'delivered', NULL, 70),
(91, 19, '2025-12-04', 'returned', NULL, 102),
(92, 17, '2025-12-07', 'delivered', NULL, 109),
(93, 19, '2025-12-07', 'delivered', NULL, 25),
(94, 32, '2025-12-09', 'delivered', NULL, 82),
(95, 35, '2025-12-11', 'delivered', NULL, 25),
(96, 13, '2025-12-12', 'delivered', NULL, 307),
(97, 17, '2025-12-14', 'delivered', NULL, 294),
(98, 17, '2025-12-16', 'delivered', NULL, 178),
(99, 14, '2025-12-18', 'delivered', NULL, 129),
(100, 7, '2025-12-19', 'delivered', NULL, 174),
(101, 18, '2025-12-19', 'delivered', NULL, 178),
(102, 25, '2025-12-21', 'cancelled', NULL, 792),
(103, 27, '2025-12-21', 'returned', NULL, 161),
(104, 32, '2025-12-21', 'delivered', NULL, 19),
(105, 18, '2025-12-23', 'delivered', NULL, 199),
(106, 34, '2025-12-24', 'returned', NULL, 319),
(107, 8, '2025-12-25', 'delivered', NULL, 551);
CREATE TABLE order_items (
    order_id    INTEGER,
    product_id  INTEGER,
    quantity    INTEGER,
    price       INTEGER
);
INSERT INTO order_items VALUES
(1, 11, 1, 41),
(2, 5, 1, 139),
(3, 4, 2, 119),
(3, 3, 2, 29),
(4, 3, 3, 29),
(5, 5, 1, 139),
(6, 3, 1, 29),
(7, 14, 2, 19),
(7, 11, 1, 41),
(8, 9, 1, 15),
(9, 6, 1, 45),
(10, 7, 1, 39),
(11, 13, 1, 129),
(12, 7, 1, 39),
(13, 13, 2, 129),
(14, 8, 2, 25),
(14, 14, 1, 19),
(15, 1, 1, 89),
(16, 14, 1, 19),
(17, 8, 2, 25),
(17, 1, 1, 89),
(17, 6, 1, 45),
(18, 4, 1, 119),
(19, 9, 3, 15),
(20, 9, 2, 15),
(21, 7, 1, 39),
(22, 7, 1, 39),
(22, 11, 1, 41),
(23, 3, 2, 29),
(24, 1, 1, 89),
(25, 9, 1, 15),
(25, 5, 2, 139),
(25, 6, 1, 45),
(26, 7, 1, 39),
(26, 10, 3, 32),
(27, 7, 1, 39),
(28, 10, 1, 32),
(29, 6, 1, 45),
(30, 13, 1, 129),
(31, 11, 1, 41),
(32, 14, 1, 19),
(32, 12, 1, 35),
(32, 3, 1, 29),
(33, 3, 1, 29),
(34, 3, 1, 29),
(34, 7, 1, 39),
(34, 4, 1, 119),
(35, 6, 1, 45),
(36, 11, 1, 41),
(37, 13, 1, 129),
(38, 10, 3, 32),
(39, 3, 1, 29),
(40, 4, 1, 119),
(41, 8, 1, 25),
(42, 10, 1, 32),
(43, 7, 1, 39),
(43, 1, 1, 89),
(44, 10, 1, 32),
(45, 13, 2, 129),
(46, 5, 1, 139),
(46, 7, 2, 39),
(47, 3, 1, 29),
(47, 6, 1, 45),
(48, 8, 2, 25),
(48, 13, 2, 129),
(48, 11, 1, 41),
(49, 2, 2, 249),
(49, 13, 2, 129),
(50, 12, 1, 35),
(51, 1, 1, 89),
(51, 8, 1, 25),
(52, 10, 1, 32),
(53, 8, 1, 25),
(54, 8, 1, 25),
(54, 2, 2, 249),
(55, 3, 3, 29),
(56, 2, 1, 249),
(57, 10, 1, 32),
(57, 3, 1, 29),
(58, 14, 1, 19),
(59, 10, 1, 32),
(60, 11, 1, 41),
(61, 5, 1, 139),
(61, 1, 2, 89),
(62, 13, 2, 129),
(63, 5, 3, 139),
(64, 11, 1, 41),
(64, 5, 2, 139),
(65, 3, 1, 29),
(66, 4, 3, 119),
(67, 6, 1, 45),
(67, 1, 1, 89),
(68, 3, 1, 29),
(69, 4, 1, 119),
(69, 12, 1, 35),
(70, 3, 1, 29),
(70, 1, 1, 89),
(70, 13, 2, 129),
(71, 1, 1, 89),
(72, 10, 1, 32),
(72, 8, 1, 25),
(73, 1, 1, 89),
(74, 3, 1, 29),
(75, 3, 1, 29),
(75, 4, 1, 119),
(75, 8, 1, 25),
(76, 12, 1, 35),
(76, 4, 1, 119),
(77, 9, 1, 15),
(78, 13, 1, 129),
(78, 14, 1, 19),
(78, 10, 2, 32),
(79, 3, 1, 29),
(80, 3, 1, 29),
(81, 14, 1, 19),
(82, 10, 1, 32),
(83, 1, 1, 89),
(83, 7, 2, 39),
(84, 11, 1, 41),
(85, 6, 1, 45),
(86, 12, 1, 35),
(86, 11, 2, 41),
(86, 13, 1, 129),
(87, 1, 2, 89),
(87, 8, 1, 25),
(87, 14, 1, 19),
(88, 5, 2, 139),
(88, 11, 2, 41),
(89, 5, 2, 139),
(89, 9, 1, 15),
(90, 14, 2, 19),
(90, 10, 1, 32),
(91, 12, 2, 35),
(91, 10, 1, 32),
(92, 14, 1, 19),
(92, 6, 2, 45),
(93, 8, 1, 25),
(94, 8, 2, 25),
(94, 10, 1, 32),
(95, 8, 1, 25),
(96, 3, 1, 29),
(96, 5, 2, 139),
(97, 6, 1, 45),
(97, 2, 1, 249),
(98, 1, 2, 89),
(99, 13, 1, 129),
(100, 5, 1, 139),
(100, 12, 1, 35),
(101, 1, 2, 89),
(102, 2, 3, 249),
(102, 6, 1, 45),
(103, 10, 1, 32),
(103, 13, 1, 129),
(104, 14, 1, 19),
(105, 9, 1, 15),
(105, 6, 1, 45),
(105, 5, 1, 139),
(106, 2, 1, 249),
(106, 12, 2, 35),
(107, 13, 3, 129),
(107, 8, 1, 25),
(107, 5, 1, 139);"""

COURSE = {
    # Two courses on one site: the lessons say which one they belong to ("track"; "base" when missing)
    "tracks": [
        {"id": "base", "title": {"en": "SQL Foundations", "ru": "Основы SQL"}},
        {"id": "analyst", "title": {"en": "SQL for Analytics", "ru": "SQL для аналитиков"},
         "about": {"en": "Business questions about one online shop", "ru": "Вопросы бизнеса про один интернет-магазин"}},
    ],
    "seeds": {"shop": SHOP_SEED},
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
        {'id': 14,
         'available': True,
         'title': {'en': 'Logic Foundations', 'ru': 'Логический фундамент'},
         'topics': {'en': 'TRUE and FALSE, AND/OR/NOT, truth tables, order, brackets', 'ru': 'TRUE и FALSE, AND/OR/NOT, таблицы истинности, порядок, скобки'},
         'theory': {'en': '<p>Every condition in <code>WHERE</code> is a small calculation whose answer is <code>TRUE</code> or <code>FALSE</code>. This lesson is about these '
                          'calculations, mostly without tables.</p>\n'
                          '<h4>Logical values</h4>\n'
                          '<ul>\n'
                          "  <li>A comparison (<code>5 &gt; 3</code>, <code>city = 'Paris'</code>) gives <code>TRUE</code> or <code>FALSE</code>. In SQLite <code>TRUE</code> is 1 and "
                          '<code>FALSE</code> is 0.</li>\n'
                          '  <li><code>AND</code> — <code>TRUE</code> only if both sides are <code>TRUE</code>. <code>OR</code> — <code>TRUE</code> if at least one side is. '
                          '<code>NOT</code> — the opposite.</li>\n'
                          '</ul>\n'
                          '<h4>The order</h4>\n'
                          '<p>Comparisons → <code>NOT</code> → <code>AND</code> → <code>OR</code>, like × before + in math. Brackets are worked out first.</p>\n'
                          '<h4>How the tasks work</h4>\n'
                          '<ul>\n'
                          '  <li><b>What does it return?</b> — choose <code>TRUE</code> or <code>FALSE</code> (in the last section also <code>NULL</code>). Then the real answer appears, '
                          'and <b>Explain condition</b> shows every step as a column.</li>\n'
                          '  <li><b>Truth table</b> — click the cells to fill them in, then press <b>Check</b>.</li>\n'
                          '  <li>Some tasks are ordinary queries.</li>\n'
                          '</ul>',
                    'ru': '<p>Каждое условие в <code>WHERE</code> — это маленькое вычисление, ответ которого <code>TRUE</code> или <code>FALSE</code>. Этот урок про такие вычисления, в '
                          'основном без таблиц.</p>\n'
                          '<h4>Логические значения</h4>\n'
                          '<ul>\n'
                          "  <li>Сравнение (<code>5 &gt; 3</code>, <code>city = 'Paris'</code>) даёт <code>TRUE</code> или <code>FALSE</code>. В SQLite <code>TRUE</code> — это 1, а "
                          '<code>FALSE</code> — 0.</li>\n'
                          '  <li><code>AND</code> — <code>TRUE</code>, только если обе стороны <code>TRUE</code>. <code>OR</code> — <code>TRUE</code>, если хотя бы одна. <code>NOT</code> '
                          '— наоборот.</li>\n'
                          '</ul>\n'
                          '<h4>Порядок</h4>\n'
                          '<p>Сравнения → <code>NOT</code> → <code>AND</code> → <code>OR</code>, как × раньше + в математике. Скобки считаются первыми.</p>\n'
                          '<h4>Как устроены задания</h4>\n'
                          '<ul>\n'
                          '  <li><b>Что вернёт?</b> — выбери <code>TRUE</code> или <code>FALSE</code> (в последнем разделе ещё <code>NULL</code>). Потом появится настоящий ответ, а '
                          'кнопка <b>«Разобрать условие»</b> покажет каждый шаг отдельным столбцом.</li>\n'
                          '  <li><b>Таблица истинности</b> — нажимай на клетки, чтобы заполнить их, потом нажми <b>«Проверить»</b>.</li>\n'
                          '  <li>Некоторые задания — обычные запросы.</li>\n'
                          '</ul>'},
         'tips': {'en': ['Ask Rosa to say the steps aloud: “first the comparisons, then NOT, then AND, then OR”.',
                         'After every answer press <b>Explain condition</b>: each step becomes a ✓/✗ column.',
                         'Math analogy: <code>AND</code> = ×, <code>OR</code> = + (TRUE = 1, FALSE = 0). <code>1 + 1 × 0</code> is 1, not 0.',
                         'In section C compare the 1/0 column with the <code>WHERE</code> result: the rows with 1 are exactly the rows <code>WHERE</code> keeps.',
                         'In section F invent your own life examples together: what she needs to go to the cinema, to a party, etc.',
                         'Section G (NULL) can wait if she is tired.'],
                  'ru': ['Проси Розу проговаривать шаги вслух: «сначала сравнения, потом NOT, потом AND, потом OR».',
                         'После каждого ответа нажимай <b>«Разобрать условие»</b>: каждый шаг станет столбцом ✓/✗.',
                         'Аналогия с математикой: <code>AND</code> = ×, <code>OR</code> = + (TRUE = 1, FALSE = 0). <code>1 + 1 × 0</code> — это 1, а не 0.',
                         'В разделе C сравни столбец 1/0 с результатом <code>WHERE</code>: строки с 1 — ровно те, которые оставляет <code>WHERE</code>.',
                         'В разделе F придумайте вместе свои жизненные примеры: что нужно, чтобы пойти в кино, на вечеринку и т. п.',
                         'Раздел G (NULL) можно отложить, если она устала.']},
         'tables': ['employees'],
         'seed': 'CREATE TABLE employees (\n'
                 '    emp_id      INT PRIMARY KEY,\n'
                 '    first_name  VARCHAR(50),\n'
                 '    last_name   VARCHAR(50),\n'
                 '    department  VARCHAR(30),\n'
                 '    salary      INT,\n'
                 '    hire_year   INT,\n'
                 '    city        VARCHAR(50),\n'
                 '    bonus       INT\n'
                 ');\n'
                 'INSERT INTO employees VALUES\n'
                 "(1,  'Alice',   'Brown',   'IT',      60000, 2018, 'London',  5000),\n"
                 "(2,  'Bob',     'Smith',   'HR',      45000, 2019, 'Paris',   NULL),\n"
                 "(3,  'Charlie', 'Johnson', 'IT',      75000, 2015, 'London',  8000),\n"
                 "(4,  'Diana',   'Miller',  'Sales',   52000, 2020, 'Berlin',  3000),\n"
                 "(5,  'Ethan',   'Davis',   'IT',      68000, 2017, 'Paris',   NULL),\n"
                 "(6,  'Fiona',   'Wilson',  'Sales',   48000, 2021, 'Madrid',  2000),\n"
                 "(7,  'George',  'Moore',   'HR',      55000, 2016, 'Berlin',  4000),\n"
                 "(8,  'Hannah',  'Taylor',  'Sales',   62000, 2018, 'London',  6000),\n"
                 "(9,  'Ivan',    'Petrov',  'IT',      90000, 2014, 'Madrid',  10000),\n"
                 "(10, 'Julia',   'Adams',   'HR',      41000, 2022, 'Paris',   NULL);",
         'tasks': [{'id': 'lg.1',
                    'kind': 'value',
                    'expr': '5 > 3',
                    'text': {'en': 'What does this expression return?', 'ru': 'Что вернёт это выражение?'},
                    'explain': {'en': '5 is greater than 3, so the answer is “yes”: <code>TRUE</code>. In the grid it is <code>1</code>.',
                                'ru': '5 больше 3, значит ответ «да»: <code>TRUE</code>. В таблице это <code>1</code>.'},
                    'section': {'en': 'A · TRUE and FALSE', 'ru': 'A · TRUE и FALSE'},
                    'intro': {'en': '<p>A comparison is a question with two possible answers: yes or no. In SQL the answer is a <b>logical value</b> (boolean): <code>TRUE</code> or '
                                    '<code>FALSE</code>. <code>5 &gt; 3</code> <i>is</i> the value <code>TRUE</code>, just like <code>2 + 3</code> <i>is</i> the value '
                                    '<code>5</code>.</p>\n'
                                    '<p>SQLite keeps <code>TRUE</code> as <code>1</code> and <code>FALSE</code> as <code>0</code>, so in the result you will see 1 and 0.</p>\n'
                                    '<p><b>Example:</b> two comparisons at once.</p>',
                              'ru': '<p>Сравнение — это вопрос, на который есть два ответа: да или нет. В SQL ответ — это <b>логическое значение</b> (boolean): <code>TRUE</code> или '
                                    '<code>FALSE</code>. <code>5 &gt; 3</code> — <i>это и есть</i> значение <code>TRUE</code>, так же как <code>2 + 3</code> — это значение '
                                    '<code>5</code>.</p>\n'
                                    '<p>SQLite хранит <code>TRUE</code> как <code>1</code>, а <code>FALSE</code> как <code>0</code>, поэтому в результате ты увидишь 1 и 0.</p>\n'
                                    '<p><b>Пример:</b> два сравнения сразу.</p>'},
                    'example': 'SELECT 5 > 3 AS first, 2 = 7 AS second;'},
                   {'id': 'lg.2',
                    'kind': 'value',
                    'expr': "'Paris' = 'Berlin'",
                    'text': {'en': 'What does this expression return?', 'ru': 'Что вернёт это выражение?'},
                    'explain': {'en': 'The texts are different, so they are not equal: <code>FALSE</code> (in the grid <code>0</code>).',
                                'ru': 'Тексты разные, значит они не равны: <code>FALSE</code> (в таблице <code>0</code>).'}},
                   {'id': 'lg.3',
                    'kind': 'value',
                    'expr': '10 <> 10',
                    'text': {'en': 'What does this expression return?', 'ru': 'Что вернёт это выражение?'},
                    'explain': {'en': '<code>&lt;&gt;</code> means “not equal”. 10 is equal to 10, so “not equal” is <code>FALSE</code>.',
                                'ru': '<code>&lt;&gt;</code> значит «не равно». 10 равно 10, поэтому «не равно» — это <code>FALSE</code>.'}},
                   {'id': 'lg.4',
                    'kind': 'value',
                    'expr': '7 >= 7',
                    'text': {'en': 'What does this expression return?', 'ru': 'Что вернёт это выражение?'},
                    'explain': {'en': '<code>&gt;=</code> means “greater <b>or</b> equal”. 7 is not greater than 7, but it is equal, so <code>TRUE</code>.',
                                'ru': '<code>&gt;=</code> значит «больше <b>или</b> равно». 7 не больше 7, но равно, поэтому <code>TRUE</code>.'}},
                   {'id': 'lg.5',
                    'kind': 'value',
                    'expr': "'apple' < 'banana'",
                    'text': {'en': 'What does this expression return?', 'ru': 'Что вернёт это выражение?'},
                    'explain': {'en': 'Texts are compared alphabetically, like in a dictionary: <i>apple</i> comes before <i>banana</i>, so it is “smaller”: <code>TRUE</code>.',
                                'ru': 'Тексты сравниваются по алфавиту, как в словаре: <i>apple</i> идёт раньше <i>banana</i>, значит он «меньше»: <code>TRUE</code>.'}},
                   {'id': 'lg.6',
                    'kind': 'truth',
                    'vars': ['A', 'B'],
                    'cols': ['A AND B'],
                    'text': {'en': 'Fill in the truth table of <code>AND</code>: what is <code>A AND B</code> for every pair of values?',
                             'ru': 'Заполни таблицу истинности для <code>AND</code>: чему равно <code>A AND B</code> для каждой пары значений?'},
                    'explain': {'en': '<code>AND</code> is <code>TRUE</code> only in the first row, where both are <code>TRUE</code>.',
                                'ru': '<code>AND</code> даёт <code>TRUE</code> только в первой строке, где оба <code>TRUE</code>.'},
                    'section': {'en': 'B · AND, OR, NOT', 'ru': 'B · AND, OR, NOT'},
                    'intro': {'en': '<p>Logical values can be joined, like numbers with + and ×:</p>\n'
                                    '<ul>\n'
                                    '<li><code>AND</code> is <code>TRUE</code> only if <b>both</b> sides are <code>TRUE</code>.</li>\n'
                                    '<li><code>OR</code> is <code>TRUE</code> if <b>at least one</b> side is <code>TRUE</code>.</li>\n'
                                    '<li><code>NOT</code> turns <code>TRUE</code> into <code>FALSE</code> and back.</li>\n'
                                    '</ul>\n'
                                    '<p>All the cases fit in a small <b>truth table</b>:</p>\n'
                                    '<table class="ops"><thead><tr><th>A</th><th>B</th><th>A AND B</th><th>A OR B</th></tr></thead><tbody>\n'
                                    '<tr><td>TRUE</td><td>TRUE</td><td>TRUE</td><td>TRUE</td></tr>\n'
                                    '<tr><td>TRUE</td><td>FALSE</td><td>FALSE</td><td>TRUE</td></tr>\n'
                                    '<tr><td>FALSE</td><td>TRUE</td><td>FALSE</td><td>TRUE</td></tr>\n'
                                    '<tr><td>FALSE</td><td>FALSE</td><td>FALSE</td><td>FALSE</td></tr>\n'
                                    '</tbody></table>\n'
                                    '<table class="ops"><thead><tr><th>A</th><th>NOT A</th></tr></thead><tbody>\n'
                                    '<tr><td>TRUE</td><td>FALSE</td></tr>\n'
                                    '<tr><td>FALSE</td><td>TRUE</td></tr>\n'
                                    '</tbody></table>\n'
                                    '<p><b>Example:</b></p>',
                              'ru': '<p>Логические значения можно соединять, как числа знаками + и ×:</p>\n'
                                    '<ul>\n'
                                    '<li><code>AND</code> («и») даёт <code>TRUE</code>, только если <b>обе</b> стороны <code>TRUE</code>.</li>\n'
                                    '<li><code>OR</code> («или») даёт <code>TRUE</code>, если <b>хотя бы одна</b> сторона <code>TRUE</code>.</li>\n'
                                    '<li><code>NOT</code> («не») меняет <code>TRUE</code> на <code>FALSE</code> и обратно.</li>\n'
                                    '</ul>\n'
                                    '<p>Все случаи помещаются в маленькую <b>таблицу истинности</b>:</p>\n'
                                    '<table class="ops"><thead><tr><th>A</th><th>B</th><th>A AND B</th><th>A OR B</th></tr></thead><tbody>\n'
                                    '<tr><td>TRUE</td><td>TRUE</td><td>TRUE</td><td>TRUE</td></tr>\n'
                                    '<tr><td>TRUE</td><td>FALSE</td><td>FALSE</td><td>TRUE</td></tr>\n'
                                    '<tr><td>FALSE</td><td>TRUE</td><td>FALSE</td><td>TRUE</td></tr>\n'
                                    '<tr><td>FALSE</td><td>FALSE</td><td>FALSE</td><td>FALSE</td></tr>\n'
                                    '</tbody></table>\n'
                                    '<table class="ops"><thead><tr><th>A</th><th>NOT A</th></tr></thead><tbody>\n'
                                    '<tr><td>TRUE</td><td>FALSE</td></tr>\n'
                                    '<tr><td>FALSE</td><td>TRUE</td></tr>\n'
                                    '</tbody></table>\n'
                                    '<p><b>Пример:</b></p>'},
                    'example': 'SELECT TRUE AND FALSE AS "and", TRUE OR FALSE AS "or", NOT TRUE AS "not";'},
                   {'id': 'lg.7',
                    'kind': 'truth',
                    'vars': ['A', 'B'],
                    'cols': ['A OR B'],
                    'text': {'en': 'Fill in the truth table of <code>OR</code>.', 'ru': 'Заполни таблицу истинности для <code>OR</code>.'},
                    'explain': {'en': '<code>OR</code> is <code>FALSE</code> only in the last row, where both are <code>FALSE</code>.',
                                'ru': '<code>OR</code> даёт <code>FALSE</code> только в последней строке, где оба <code>FALSE</code>.'}},
                   {'id': 'lg.8',
                    'kind': 'truth',
                    'vars': ['A'],
                    'cols': ['NOT A'],
                    'text': {'en': 'Fill in the truth table of <code>NOT</code>.', 'ru': 'Заполни таблицу истинности для <code>NOT</code>.'}},
                   {'id': 'lg.9',
                    'kind': 'value',
                    'expr': 'TRUE AND FALSE',
                    'text': {'en': 'What does this expression return?', 'ru': 'Что вернёт это выражение?'},
                    'explain': {'en': '<code>AND</code> needs both sides <code>TRUE</code>. The right side is <code>FALSE</code>, so the result is <code>FALSE</code>.',
                                'ru': '<code>AND</code> нужны обе стороны <code>TRUE</code>. Справа <code>FALSE</code>, поэтому результат <code>FALSE</code>.'}},
                   {'id': 'lg.10',
                    'kind': 'value',
                    'expr': 'FALSE OR TRUE',
                    'text': {'en': 'What does this expression return?', 'ru': 'Что вернёт это выражение?'},
                    'explain': {'en': '<code>OR</code> needs at least one <code>TRUE</code>. The right side is <code>TRUE</code>, so <code>TRUE</code>.',
                                'ru': '<code>OR</code> хватает одного <code>TRUE</code>. Справа <code>TRUE</code>, значит <code>TRUE</code>.'}},
                   {'id': 'lg.11',
                    'kind': 'value',
                    'expr': 'NOT (3 > 5)',
                    'text': {'en': 'What does this expression return?', 'ru': 'Что вернёт это выражение?'},
                    'explain': {'en': '<code>3 &gt; 5</code> is <code>FALSE</code>. <code>NOT</code> turns <code>FALSE</code> into <code>TRUE</code>.',
                                'ru': '<code>3 &gt; 5</code> — это <code>FALSE</code>. <code>NOT</code> меняет <code>FALSE</code> на <code>TRUE</code>.'}},
                   {'id': 'lg.12',
                    'kind': 'value',
                    'expr': 'TRUE AND TRUE AND FALSE',
                    'text': {'en': 'What does this expression return?', 'ru': 'Что вернёт это выражение?'},
                    'explain': {'en': 'With several <code>AND</code> all parts must be <code>TRUE</code>. One <code>FALSE</code> is enough to make everything <code>FALSE</code>.',
                                'ru': 'Когда <code>AND</code> несколько, все части должны быть <code>TRUE</code>. Одного <code>FALSE</code> достаточно, чтобы всё стало '
                                      '<code>FALSE</code>.'}},
                   {'id': 'lg.13',
                    'kind': 'value',
                    'expr': 'FALSE OR FALSE OR TRUE',
                    'text': {'en': 'What does this expression return?', 'ru': 'Что вернёт это выражение?'},
                    'explain': {'en': 'With several <code>OR</code> one <code>TRUE</code> is enough: <code>TRUE</code>.',
                                'ru': 'Когда <code>OR</code> несколько, хватает одного <code>TRUE</code>: <code>TRUE</code>.'}},
                   {'id': 'lg.14',
                    'kind': 'value',
                    'expr': '5 > 3 AND 2 > 7',
                    'text': {'en': 'What does this expression return?', 'ru': 'Что вернёт это выражение?'},
                    'explain': {'en': 'The comparisons first: <code>5 &gt; 3</code> is <code>TRUE</code>, <code>2 &gt; 7</code> is <code>FALSE</code>. <code>TRUE AND FALSE</code> = '
                                      '<code>FALSE</code>.',
                                'ru': 'Сначала сравнения: <code>5 &gt; 3</code> — <code>TRUE</code>, <code>2 &gt; 7</code> — <code>FALSE</code>. <code>TRUE AND FALSE</code> = '
                                      '<code>FALSE</code>.'}},
                   {'id': 'lg.15',
                    'kind': 'truth',
                    'vars': ['A', 'B'],
                    'cols': ['NOT B', 'A AND NOT B'],
                    'text': {'en': 'Fill in both columns. The first one is a step that helps with the second.', 'ru': 'Заполни оба столбца. Первый — это шаг, который помогает со вторым.'},
                    'explain': {'en': '<code>A AND NOT B</code> is <code>TRUE</code> only when <code>A</code> is <code>TRUE</code> and <code>B</code> is <code>FALSE</code>.',
                                'ru': '<code>A AND NOT B</code> даёт <code>TRUE</code>, только когда <code>A</code> — <code>TRUE</code>, а <code>B</code> — <code>FALSE</code>.'}},
                   {'id': 'lg.16',
                    'text': {'en': "Show <code>first_name</code>, <code>city</code> and a column <code>is_paris</code> that says whether the employee is from <code>'Paris'</code>.",
                             'ru': "Выведи <code>first_name</code>, <code>city</code> и столбец <code>is_paris</code>, который показывает, из <code>'Paris'</code> ли сотрудник."},
                    'answer': "SELECT first_name, city, city = 'Paris' AS is_paris FROM employees;",
                    'section': {'en': 'C · A comparison is a column', 'ru': 'C · Сравнение — это столбец'},
                    'intro': {'en': '<p>A comparison can be a column of the result. Then every row gets its own answer, 1 or 0, like a helper column in Excel with '
                                    '<code>=C2&gt;60000</code>.</p>\n'
                                    '<p><code>WHERE</code> does the same comparison for every row and keeps only the rows where the answer is 1 (<code>TRUE</code>).</p>\n'
                                    '<p><b>Example:</b> who earns more than 60000.</p>',
                              'ru': '<p>Сравнение может быть столбцом результата. Тогда у каждой строки свой ответ, 1 или 0, как вспомогательный столбец в Excel с формулой '
                                    '<code>=C2&gt;60000</code>.</p>\n'
                                    '<p><code>WHERE</code> делает то же сравнение для каждой строки и оставляет только строки, где ответ 1 (<code>TRUE</code>).</p>\n'
                                    '<p><b>Пример:</b> кто зарабатывает больше 60000.</p>'},
                    'example': 'SELECT first_name, salary, salary > 60000 AS rich\nFROM employees;'},
                   {'id': 'lg.17',
                    'text': {'en': "Show <code>first_name</code>, <code>department</code>, <code>salary</code> and two columns: <code>is_it</code> (the department is <code>'IT'</code>) "
                                   'and <code>high</code> (salary greater than 60000).',
                             'ru': "Выведи <code>first_name</code>, <code>department</code>, <code>salary</code> и два столбца: <code>is_it</code> (отдел <code>'IT'</code>) и "
                                   '<code>high</code> (зарплата больше 60000).'},
                    'answer': "SELECT first_name, department, salary,\n       department = 'IT' AS is_it,\n       salary > 60000 AS high\nFROM employees;"},
                   {'id': 'lg.18',
                    'text': {'en': "Join the two conditions: show <code>first_name</code> and a column <code>it_and_high</code> = the department is <code>'IT'</code> AND salary greater "
                                   'than 60000.',
                             'ru': "Соедини два условия: выведи <code>first_name</code> и столбец <code>it_and_high</code> = отдел <code>'IT'</code> И зарплата больше 60000."},
                    'answer': "SELECT first_name, department = 'IT' AND salary > 60000 AS it_and_high FROM employees;"},
                   {'id': 'lg.19',
                    'text': {'en': "Show <code>first_name</code>, <code>city</code> and a column <code>not_london</code>: the employee is NOT from <code>'London'</code>. Use "
                                   '<code>NOT</code>.',
                             'ru': "Выведи <code>first_name</code>, <code>city</code> и столбец <code>not_london</code>: сотрудник НЕ из <code>'London'</code>. Используй "
                                   '<code>NOT</code>.'},
                    'answer': "SELECT first_name, city, NOT city = 'London' AS not_london FROM employees;"},
                   {'id': 'lg.20',
                    'text': {'en': "Now put the condition from the previous tasks into <code>WHERE</code>: show all employees from <code>'IT'</code> with salary greater than 60000. These "
                                   'are exactly the rows where <code>it_and_high</code> was 1.',
                             'ru': "Теперь перенеси условие из прошлых заданий в <code>WHERE</code>: выведи всех сотрудников из <code>'IT'</code> с зарплатой больше 60000. Это ровно те "
                                   'строки, где <code>it_and_high</code> был 1.'},
                    'answer': "SELECT * FROM employees WHERE department = 'IT' AND salary > 60000;"},
                   {'id': 'lg.21',
                    'kind': 'value',
                    'expr': 'TRUE OR FALSE AND FALSE',
                    'text': {'en': 'What does this expression return?', 'ru': 'Что вернёт это выражение?'},
                    'explain': {'en': '<code>AND</code> goes first: <code>FALSE AND FALSE</code> = <code>FALSE</code>. Then <code>TRUE OR FALSE</code> = <code>TRUE</code>. Left to right '
                                      'you would get <code>FALSE</code>: that is the trap.',
                                'ru': 'Сначала <code>AND</code>: <code>FALSE AND FALSE</code> = <code>FALSE</code>. Потом <code>TRUE OR FALSE</code> = <code>TRUE</code>. Если считать '
                                      'слева направо, получится <code>FALSE</code>: в этом и ловушка.'},
                    'section': {'en': 'D · Who goes first: NOT, AND, OR', 'ru': 'D · Кто первый: NOT, AND, OR'},
                    'intro': {'en': '<p>Like in math, where × goes before +, logical operators have an order:</p>\n'
                                    '<ol>\n'
                                    '<li>comparisons (<code>=</code>, <code>&gt;</code>, <code>&lt;&gt;</code>, …)</li>\n'
                                    '<li><code>NOT</code></li>\n'
                                    '<li><code>AND</code></li>\n'
                                    '<li><code>OR</code></li>\n'
                                    '</ol>\n'
                                    '<p>Think of <code>AND</code> as × and <code>OR</code> as + (<code>TRUE</code> = 1, <code>FALSE</code> = 0): <code>TRUE OR TRUE AND FALSE</code> = 1 + '
                                    '1 × 0 = 1 = <code>TRUE</code>. <code>NOT</code> is like a minus in front of a number: it acts only on the nearest value.</p>\n'
                                    '<p><b>Example:</b> math and logic follow the same idea.</p>',
                              'ru': '<p>Как в математике, где × выполняется раньше +, у логических операторов есть порядок:</p>\n'
                                    '<ol>\n'
                                    '<li>сравнения (<code>=</code>, <code>&gt;</code>, <code>&lt;&gt;</code>, …)</li>\n'
                                    '<li><code>NOT</code></li>\n'
                                    '<li><code>AND</code></li>\n'
                                    '<li><code>OR</code></li>\n'
                                    '</ol>\n'
                                    '<p>Представь <code>AND</code> как ×, а <code>OR</code> как + (<code>TRUE</code> = 1, <code>FALSE</code> = 0): <code>TRUE OR TRUE AND FALSE</code> = 1 '
                                    '+ 1 × 0 = 1 = <code>TRUE</code>. <code>NOT</code> — как минус перед числом: действует только на ближайшее значение.</p>\n'
                                    '<p><b>Пример:</b> в математике и в логике одна и та же идея.</p>'},
                    'example': 'SELECT 1 + 2 * 3 AS math, TRUE OR TRUE AND FALSE AS logic;'},
                   {'id': 'lg.22',
                    'kind': 'value',
                    'expr': '2 < 4 OR 3 > 5 AND 1 = 2',
                    'text': {'en': 'What does this expression return?', 'ru': 'Что вернёт это выражение?'},
                    'explain': {'en': 'Comparisons first: <code>TRUE OR FALSE AND FALSE</code>. Then <code>AND</code>: <code>FALSE AND FALSE</code> = <code>FALSE</code>. Then '
                                      '<code>OR</code>: <code>TRUE OR FALSE</code> = <code>TRUE</code>.',
                                'ru': 'Сначала сравнения: <code>TRUE OR FALSE AND FALSE</code>. Потом <code>AND</code>: <code>FALSE AND FALSE</code> = <code>FALSE</code>. Потом '
                                      '<code>OR</code>: <code>TRUE OR FALSE</code> = <code>TRUE</code>.'}},
                   {'id': 'lg.23',
                    'kind': 'value',
                    'expr': 'NOT TRUE AND FALSE',
                    'text': {'en': 'What does this expression return?', 'ru': 'Что вернёт это выражение?'},
                    'explain': {'en': '<code>NOT</code> acts only on the nearest value: <code>(NOT TRUE) AND FALSE</code> = <code>FALSE AND FALSE</code> = <code>FALSE</code>. It is not '
                                      '<code>NOT (TRUE AND FALSE)</code>, which would be <code>TRUE</code>.',
                                'ru': '<code>NOT</code> действует только на ближайшее значение: <code>(NOT TRUE) AND FALSE</code> = <code>FALSE AND FALSE</code> = <code>FALSE</code>. Это '
                                      'не <code>NOT (TRUE AND FALSE)</code>, которое было бы <code>TRUE</code>.'}},
                   {'id': 'lg.24',
                    'kind': 'value',
                    'expr': 'NOT FALSE OR TRUE',
                    'text': {'en': 'What does this expression return?', 'ru': 'Что вернёт это выражение?'},
                    'explain': {'en': '<code>(NOT FALSE) OR TRUE</code> = <code>TRUE OR TRUE</code> = <code>TRUE</code>. <code>NOT</code> does not cover the whole <code>OR</code>.',
                                'ru': '<code>(NOT FALSE) OR TRUE</code> = <code>TRUE OR TRUE</code> = <code>TRUE</code>. <code>NOT</code> не действует на весь <code>OR</code>.'}},
                   {'id': 'lg.25',
                    'kind': 'value',
                    'expr': 'NOT 5 > 3 OR 2 > 1',
                    'text': {'en': 'What does this expression return?', 'ru': 'Что вернёт это выражение?'},
                    'explain': {'en': 'Comparisons first: <code>NOT TRUE OR TRUE</code>. Then <code>NOT</code>: <code>FALSE OR TRUE</code>. Then <code>OR</code>: <code>TRUE</code>.',
                                'ru': 'Сначала сравнения: <code>NOT TRUE OR TRUE</code>. Потом <code>NOT</code>: <code>FALSE OR TRUE</code>. Потом <code>OR</code>: <code>TRUE</code>.'}},
                   {'id': 'lg.26',
                    'kind': 'value',
                    'expr': 'TRUE OR TRUE AND NOT TRUE',
                    'text': {'en': 'What does this expression return?', 'ru': 'Что вернёт это выражение?'},
                    'explain': {'en': '<code>NOT</code> first: <code>NOT TRUE</code> = <code>FALSE</code>. Then <code>AND</code>: <code>TRUE AND FALSE</code> = <code>FALSE</code>. Then '
                                      '<code>OR</code>: <code>TRUE OR FALSE</code> = <code>TRUE</code>.',
                                'ru': 'Сначала <code>NOT</code>: <code>NOT TRUE</code> = <code>FALSE</code>. Потом <code>AND</code>: <code>TRUE AND FALSE</code> = <code>FALSE</code>. '
                                      'Потом <code>OR</code>: <code>TRUE OR FALSE</code> = <code>TRUE</code>.'}},
                   {'id': 'lg.27',
                    'kind': 'truth',
                    'vars': ['A', 'B', 'C'],
                    'cols': ['B AND C', 'A OR B AND C'],
                    'text': {'en': 'Fill in both columns. The first one is the part SQL works out first.', 'ru': 'Заполни оба столбца. Первый — это часть, которую SQL считает первой.'},
                    'explain': {'en': '<code>A OR B AND C</code> = <code>A OR (B AND C)</code>: it is <code>TRUE</code> when <code>A</code> is <code>TRUE</code>, or when the first column '
                                      'is <code>TRUE</code>.',
                                'ru': '<code>A OR B AND C</code> = <code>A OR (B AND C)</code>: это <code>TRUE</code>, когда <code>A</code> — <code>TRUE</code> или когда первый столбец '
                                      '<code>TRUE</code>.'}},
                   {'id': 'lg.28',
                    'kind': 'value',
                    'expr': '(TRUE OR FALSE) AND FALSE',
                    'text': {'en': 'What does this expression return?', 'ru': 'Что вернёт это выражение?'},
                    'explain': {'en': 'Brackets first: <code>TRUE OR FALSE</code> = <code>TRUE</code>. Then <code>TRUE AND FALSE</code> = <code>FALSE</code>. Without brackets it would be '
                                      '<code>TRUE</code>.',
                                'ru': 'Сначала скобки: <code>TRUE OR FALSE</code> = <code>TRUE</code>. Потом <code>TRUE AND FALSE</code> = <code>FALSE</code>. Без скобок было бы '
                                      '<code>TRUE</code>.'},
                    'section': {'en': 'E · Brackets', 'ru': 'E · Скобки'},
                    'intro': {'en': '<p>Brackets change the order, like in math: what is in brackets is worked out first. <code>(TRUE OR FALSE) AND FALSE</code> = <code>TRUE AND '
                                    'FALSE</code> = <code>FALSE</code>, but without the brackets the same values give <code>TRUE</code>.</p>\n'
                                    '<p><code>NOT (…)</code> turns around the whole bracket, <code>NOT</code> without brackets only the nearest value.</p>\n'
                                    '<p>Rule: if you mix <code>AND</code> and <code>OR</code>, write the brackets, even where they are not needed. Then the query is easy to read and to '
                                    'check.</p>\n'
                                    '<p><b>Example:</b> <code>NOT</code> without and with brackets.</p>',
                              'ru': '<p>Скобки меняют порядок, как в математике: то, что в скобках, считается первым. <code>(TRUE OR FALSE) AND FALSE</code> = <code>TRUE AND FALSE</code> '
                                    '= <code>FALSE</code>, а без скобок те же значения дают <code>TRUE</code>.</p>\n'
                                    '<p><code>NOT (…)</code> переворачивает всю скобку, а <code>NOT</code> без скобок — только ближайшее значение.</p>\n'
                                    '<p>Правило: если смешиваешь <code>AND</code> и <code>OR</code>, ставь скобки, даже там, где они не обязательны. Так запрос легко читать и '
                                    'проверять.</p>\n'
                                    '<p><b>Пример:</b> <code>NOT</code> без скобок и со скобками.</p>'},
                    'example': 'SELECT NOT TRUE OR TRUE AS without_brackets,\n       NOT (TRUE OR TRUE) AS with_brackets;'},
                   {'id': 'lg.29',
                    'kind': 'value',
                    'expr': 'NOT (TRUE AND FALSE)',
                    'text': {'en': 'What does this expression return?', 'ru': 'Что вернёт это выражение?'},
                    'explain': {'en': 'Brackets first: <code>TRUE AND FALSE</code> = <code>FALSE</code>. <code>NOT FALSE</code> = <code>TRUE</code>.',
                                'ru': 'Сначала скобки: <code>TRUE AND FALSE</code> = <code>FALSE</code>. <code>NOT FALSE</code> = <code>TRUE</code>.'}},
                   {'id': 'lg.30',
                    'kind': 'value',
                    'expr': 'NOT (FALSE OR TRUE) AND TRUE',
                    'text': {'en': 'What does this expression return?', 'ru': 'Что вернёт это выражение?'},
                    'explain': {'en': 'Brackets: <code>FALSE OR TRUE</code> = <code>TRUE</code>. <code>NOT TRUE</code> = <code>FALSE</code>. <code>FALSE AND TRUE</code> = '
                                      '<code>FALSE</code>.',
                                'ru': 'Скобки: <code>FALSE OR TRUE</code> = <code>TRUE</code>. <code>NOT TRUE</code> = <code>FALSE</code>. <code>FALSE AND TRUE</code> = '
                                      '<code>FALSE</code>.'}},
                   {'id': 'lg.31',
                    'kind': 'value',
                    'expr': '(2 < 4 OR 3 > 5) AND 1 = 2',
                    'text': {'en': 'What does this expression return?', 'ru': 'Что вернёт это выражение?'},
                    'explain': {'en': 'The same comparisons as in section D, but with brackets: <code>(TRUE OR FALSE) AND FALSE</code> = <code>TRUE AND FALSE</code> = <code>FALSE</code>. '
                                      'The brackets changed the answer.',
                                'ru': 'Те же сравнения, что в разделе D, но со скобками: <code>(TRUE OR FALSE) AND FALSE</code> = <code>TRUE AND FALSE</code> = <code>FALSE</code>. Скобки '
                                      'поменяли ответ.'}},
                   {'id': 'lg.32',
                    'kind': 'truth',
                    'vars': ['A', 'B', 'C'],
                    'cols': ['A OR B AND C', '(A OR B) AND C'],
                    'text': {'en': 'Fill in both columns. In which rows are they different?', 'ru': 'Заполни оба столбца. В каких строках они отличаются?'},
                    'explain': {'en': 'They are different when <code>A</code> is <code>TRUE</code> and <code>C</code> is <code>FALSE</code>: without brackets <code>A</code> alone is '
                                      'enough, with brackets <code>C</code> is always needed.',
                                'ru': 'Они отличаются, когда <code>A</code> — <code>TRUE</code>, а <code>C</code> — <code>FALSE</code>: без скобок хватает одного <code>A</code>, а со '
                                      'скобками <code>C</code> нужен всегда.'}},
                   {'id': 'lg.33',
                    'kind': 'truth',
                    'vars': ['A', 'B'],
                    'cols': ['NOT A AND B', 'NOT (A AND B)'],
                    'text': {'en': 'Fill in both columns. Where does the bracket after <code>NOT</code> change the result?',
                             'ru': 'Заполни оба столбца. Где скобка после <code>NOT</code> меняет результат?'},
                    'explain': {'en': '<code>NOT A AND B</code> = <code>(NOT A) AND B</code>: <code>TRUE</code> only for <code>A</code> = <code>FALSE</code>, <code>B</code> = '
                                      '<code>TRUE</code>. <code>NOT (A AND B)</code> is <code>FALSE</code> only when both are <code>TRUE</code>.',
                                'ru': '<code>NOT A AND B</code> = <code>(NOT A) AND B</code>: <code>TRUE</code> только при <code>A</code> = <code>FALSE</code>, <code>B</code> = '
                                      '<code>TRUE</code>. <code>NOT (A AND B)</code> даёт <code>FALSE</code>, только когда оба <code>TRUE</code>.'}},
                  {'id': 'lg.d1',
                    'kind': 'truth',
                    'vars': ['A', 'B'],
                    'cols': ['A AND B', 'NOT (A AND B)', 'NOT A OR NOT B'],
                    'text': {'en': 'Prove the first law. Fill in the table: the columns <code>NOT (A AND B)</code> and <code>NOT A OR NOT B</code> must be the same in every row.',
                             'ru': 'Докажи первый закон. Заполни таблицу: столбцы <code>NOT (A AND B)</code> и <code>NOT A OR NOT B</code> должны совпасть в каждой строке.'},
                    'explain': {'en': 'The last two columns are the same in all 4 rows, so <code>NOT (A AND B)</code> = <code>NOT A OR NOT B</code>. Both are <code>FALSE</code> only in the first '
                                      'row.',
                                'ru': 'Два последних столбца совпадают во всех 4 строках, значит <code>NOT (A AND B)</code> = <code>NOT A OR NOT B</code>. Оба равны <code>FALSE</code> только в '
                                      'первой строке.'},
                    'section': {'en': "F · De Morgan's laws", 'ru': 'F · Законы де Моргана'},
                    'intro': {'en': "<p>De Morgan's laws show how to remove the brackets after <code>NOT</code>:</p>\n"
                                    '<pre class="code">NOT (A AND B)  =  NOT A OR  NOT B\n'
                                    'NOT (A OR  B)  =  NOT A AND NOT B</pre>\n'
                                    '<p><b>Recipe:</b> put <code>NOT</code> on each part <b>and swap</b> <code>AND</code> ↔ <code>OR</code>.</p>\n'
                                    '<p>In words: “not (rain or snow)” = “no rain <b>and</b> no snow”. “Not (tall and rich)” = “not tall <b>or</b> not rich”: one missing quality is enough.</p>\n'
                                    '<p>Why does the operator flip? <code>A AND B</code> is <code>TRUE</code> in one row only, where both are <code>TRUE</code>. So <code>NOT (A AND B)</code> is '
                                    '<code>FALSE</code> in that row only, and that is exactly the row where <code>NOT A OR NOT B</code> is <code>FALSE</code>. A truth table proves it: two '
                                    'expressions are equal if their columns match in <b>every</b> row.</p>\n'
                                    '<p>Two more rules. <code>NOT NOT A</code> = <code>A</code>. And <code>NOT</code> in front of one comparison is written with the opposite operator:</p>\n'
                                    '<table class="ops"><thead><tr><th>NOT (…)</th><th>=</th></tr></thead><tbody>\n'
                                    '<tr><td><code>NOT (x = 5)</code></td><td><code>x &lt;&gt; 5</code></td></tr>\n'
                                    '<tr><td><code>NOT (x &lt;&gt; 5)</code></td><td><code>x = 5</code></td></tr>\n'
                                    '<tr><td><code>NOT (x &gt; 5)</code></td><td><code>x &lt;= 5</code></td></tr>\n'
                                    '<tr><td><code>NOT (x &lt; 5)</code></td><td><code>x &gt;= 5</code></td></tr>\n'
                                    '<tr><td><code>NOT (x &gt;= 5)</code></td><td><code>x &lt; 5</code></td></tr>\n'
                                    '<tr><td><code>NOT (x &lt;= 5)</code></td><td><code>x &gt; 5</code></td></tr>\n'
                                    '</tbody></table>\n'
                                    '<p><b>The classic mistake</b> is to forget the swap: <code>NOT (A OR B)</code> is <b>not</b> <code>NOT A OR NOT B</code>.</p>\n'
                                    '<p><b>Example:</b> both sides of the second law on the employees table give the same column.</p>',
                              'ru': '<p>Законы де Моргана показывают, как убрать скобки после <code>NOT</code>:</p>\n'
                                    '<pre class="code">NOT (A AND B)  =  NOT A OR  NOT B\n'
                                    'NOT (A OR  B)  =  NOT A AND NOT B</pre>\n'
                                    '<p><b>Рецепт:</b> поставь <code>NOT</code> перед каждой частью <b>и поменяй</b> <code>AND</code> ↔ <code>OR</code>.</p>\n'
                                    '<p>Словами: «не (дождь или снег)» = «нет дождя <b>и</b> нет снега». «Не (высокий и богатый)» = «не высокий <b>или</b> не богатый»: достаточно, чтобы не хватало '
                                    'одного качества.</p>\n'
                                    '<p>Почему оператор меняется? <code>A AND B</code> даёт <code>TRUE</code> только в одной строке, где оба <code>TRUE</code>. Значит, <code>NOT (A AND B)</code> '
                                    'даёт <code>FALSE</code> только в этой строке, и это ровно та строка, где <code>NOT A OR NOT B</code> равно <code>FALSE</code>. Таблица истинности это '
                                    'доказывает: два выражения равны, если их столбцы совпадают в <b>каждой</b> строке.</p>\n'
                                    '<p>Ещё два правила. <code>NOT NOT A</code> = <code>A</code>. А <code>NOT</code> перед одним сравнением записывают противоположным оператором:</p>\n'
                                    '<table class="ops"><thead><tr><th>NOT (…)</th><th>=</th></tr></thead><tbody>\n'
                                    '<tr><td><code>NOT (x = 5)</code></td><td><code>x &lt;&gt; 5</code></td></tr>\n'
                                    '<tr><td><code>NOT (x &lt;&gt; 5)</code></td><td><code>x = 5</code></td></tr>\n'
                                    '<tr><td><code>NOT (x &gt; 5)</code></td><td><code>x &lt;= 5</code></td></tr>\n'
                                    '<tr><td><code>NOT (x &lt; 5)</code></td><td><code>x &gt;= 5</code></td></tr>\n'
                                    '<tr><td><code>NOT (x &gt;= 5)</code></td><td><code>x &lt; 5</code></td></tr>\n'
                                    '<tr><td><code>NOT (x &lt;= 5)</code></td><td><code>x &gt; 5</code></td></tr>\n'
                                    '</tbody></table>\n'
                                    '<p><b>Классическая ошибка</b> — забыть поменять оператор: <code>NOT (A OR B)</code> — это <b>не</b> <code>NOT A OR NOT B</code>.</p>\n'
                                    '<p><b>Пример:</b> обе стороны второго закона на таблице сотрудников дают одинаковый столбец.</p>'},
                    'example': 'SELECT first_name, city, department,\n'
                               "       NOT (city = 'Paris' OR department = 'HR') AS left_side,\n"
                               "       city <> 'Paris' AND department <> 'HR' AS right_side\n"
                               'FROM employees;'},
                   {'id': 'lg.d2',
                    'kind': 'truth',
                    'vars': ['A', 'B'],
                    'cols': ['A OR B', 'NOT (A OR B)', 'NOT A AND NOT B'],
                    'text': {'en': 'Prove the second law: fill in the table and compare the last two columns.', 'ru': 'Докажи второй закон: заполни таблицу и сравни два последних столбца.'},
                    'explain': {'en': 'The last two columns are the same in all 4 rows: both are <code>TRUE</code> only in the last row, where <code>A</code> and <code>B</code> are both '
                                      '<code>FALSE</code>.',
                                'ru': 'Два последних столбца совпадают во всех 4 строках: оба равны <code>TRUE</code> только в последней строке, где и <code>A</code>, и <code>B</code> — '
                                      '<code>FALSE</code>.'}},
                   {'id': 'lg.d3',
                    'kind': 'truth',
                    'vars': ['A', 'B'],
                    'cols': ['NOT (A OR B)', 'NOT A OR NOT B'],
                    'text': {'en': 'Someone forgot to swap <code>OR</code> for <code>AND</code>. Fill in the table: are the two columns equal?',
                             'ru': 'Кто-то забыл поменять <code>OR</code> на <code>AND</code>. Заполни таблицу: равны ли два столбца?'},
                    'explain': {'en': 'No: they differ in rows 2 and 3, where only one of <code>A</code>, <code>B</code> is <code>TRUE</code>. Without the swap the law does not work.',
                                'ru': 'Нет: они отличаются в строках 2 и 3, где <code>TRUE</code> только одно из <code>A</code>, <code>B</code>. Без замены оператора закон не работает.'}},
                   {'id': 'lg.d4',
                    'kind': 'truth',
                    'vars': ['A'],
                    'cols': ['NOT A', 'NOT NOT A'],
                    'text': {'en': 'Fill in the table. What does a double <code>NOT</code> do?', 'ru': 'Заполни таблицу. Что делает двойное <code>NOT</code>?'},
                    'explain': {'en': '<code>NOT NOT A</code> turns the value around twice, so it is <code>A</code> again.',
                                'ru': '<code>NOT NOT A</code> переворачивает значение два раза, поэтому снова получается <code>A</code>.'}},
                   {'id': 'lg.d5',
                    'kind': 'truth',
                    'vars': ['A', 'B', 'C'],
                    'cols': ['NOT (A OR B OR C)', 'NOT A AND NOT B AND NOT C'],
                    'text': {'en': 'The law works for any number of parts. Prove it for three: fill in both columns.',
                             'ru': 'Закон работает для любого числа частей. Докажи его для трёх: заполни оба столбца.'},
                    'explain': {'en': 'Both columns are <code>TRUE</code> only in the last row, where all three are <code>FALSE</code>.',
                                'ru': 'Оба столбца равны <code>TRUE</code> только в последней строке, где все три — <code>FALSE</code>.'}},
                   {'id': 'lg.d6',
                    'kind': 'rewrite',
                    'expr': 'NOT (A AND B)',
                    'vars': ['A', 'B'],
                    'form': 'no_not_bracket',
                    'text': {'en': 'Open the brackets after <code>NOT</code>: write the same condition without <code>NOT</code> in front of a bracket.',
                             'ru': 'Раскрой скобки после <code>NOT</code>: запиши то же условие без <code>NOT</code> перед скобкой.'},
                    'answer': 'NOT A OR NOT B',
                    'explain': {'en': '<code>NOT</code> on each part, <code>AND</code> becomes <code>OR</code>: <code>NOT A OR NOT B</code>.',
                                'ru': '<code>NOT</code> перед каждой частью, <code>AND</code> становится <code>OR</code>: <code>NOT A OR NOT B</code>.'},
                    'section': {'en': "G · De Morgan's laws: practice", 'ru': 'G · Законы де Моргана: практика'},
                    'intro': {'en': '<p>Now rewrite conditions yourself. Type <b>only the new condition</b> in the editor, without <code>SELECT</code>, for example <code>NOT A OR NOT B</code>, and '
                                    'press <b>Run</b>.</p>\n'
                                    '<p>The grid shows the original condition and yours side by side for every case. They must match in every row, and there must be no <code>NOT</code> in front of '
                                    'a bracket.</p>\n'
                                    '<p>In the tasks with comparisons, remove <code>NOT</code> completely: use the opposite operator (<code>=</code> ↔ <code>&lt;&gt;</code>, <code>&gt;</code> ↔ '
                                    '<code>&lt;=</code>, <code>&lt;</code> ↔ <code>&gt;=</code>).</p>\n'
                                    '<p><b>Example:</b> <code>NOT (A OR NOT B)</code> = <code>NOT A AND NOT NOT B</code> = <code>NOT A AND B</code>.</p>',
                              'ru': '<p>Теперь преобразуй условия сама. Напиши в редакторе <b>только новое условие</b>, без <code>SELECT</code>, например <code>NOT A OR NOT B</code>, и нажми '
                                    '<b>«Выполнить»</b>.</p>\n'
                                    '<p>В таблице рядом появятся исходное условие и твоё для каждого случая. Они должны совпасть в каждой строке, и перед скобкой не должно остаться '
                                    '<code>NOT</code>.</p>\n'
                                    '<p>В заданиях со сравнениями убери <code>NOT</code> совсем: используй противоположный оператор (<code>=</code> ↔ <code>&lt;&gt;</code>, <code>&gt;</code> ↔ '
                                    '<code>&lt;=</code>, <code>&lt;</code> ↔ <code>&gt;=</code>).</p>\n'
                                    '<p><b>Пример:</b> <code>NOT (A OR NOT B)</code> = <code>NOT A AND NOT NOT B</code> = <code>NOT A AND B</code>.</p>'},
                    'example': 'WITH v(A, B) AS (VALUES (TRUE, TRUE), (TRUE, FALSE), (FALSE, TRUE), (FALSE, FALSE))\nSELECT A, B, NOT (A OR NOT B) AS original, NOT A AND B AS rewritten\nFROM v;'},
                   {'id': 'lg.d7',
                    'kind': 'rewrite',
                    'expr': 'NOT (A OR B)',
                    'vars': ['A', 'B'],
                    'form': 'no_not_bracket',
                    'text': {'en': 'Open the brackets after <code>NOT</code>: write the same condition without <code>NOT</code> in front of a bracket.',
                             'ru': 'Раскрой скобки после <code>NOT</code>: запиши то же условие без <code>NOT</code> перед скобкой.'},
                    'answer': 'NOT A AND NOT B',
                    'explain': {'en': '<code>NOT</code> on each part, <code>OR</code> becomes <code>AND</code>: <code>NOT A AND NOT B</code>.',
                                'ru': '<code>NOT</code> перед каждой частью, <code>OR</code> становится <code>AND</code>: <code>NOT A AND NOT B</code>.'}},
                   {'id': 'lg.d8',
                    'kind': 'rewrite',
                    'expr': 'NOT (NOT A AND B)',
                    'vars': ['A', 'B'],
                    'form': 'no_not_bracket',
                    'text': {'en': 'Open the brackets after <code>NOT</code>: write the same condition without <code>NOT</code> in front of a bracket.',
                             'ru': 'Раскрой скобки после <code>NOT</code>: запиши то же условие без <code>NOT</code> перед скобкой.'},
                    'answer': 'A OR NOT B',
                    'explain': {'en': '<code>NOT NOT A OR NOT B</code>, and <code>NOT NOT A</code> = <code>A</code>: <code>A OR NOT B</code>.',
                                'ru': '<code>NOT NOT A OR NOT B</code>, а <code>NOT NOT A</code> = <code>A</code>: <code>A OR NOT B</code>.'}},
                   {'id': 'lg.d9',
                    'kind': 'rewrite',
                    'expr': 'NOT (A AND B AND C)',
                    'vars': ['A', 'B', 'C'],
                    'form': 'no_not_bracket',
                    'text': {'en': 'Open the brackets after <code>NOT</code>: write the same condition without <code>NOT</code> in front of a bracket.',
                             'ru': 'Раскрой скобки после <code>NOT</code>: запиши то же условие без <code>NOT</code> перед скобкой.'},
                    'answer': 'NOT A OR NOT B OR NOT C',
                    'explain': {'en': 'Every <code>AND</code> becomes <code>OR</code>: <code>NOT A OR NOT B OR NOT C</code>.',
                                'ru': 'Каждый <code>AND</code> становится <code>OR</code>: <code>NOT A OR NOT B OR NOT C</code>.'}},
                   {'id': 'lg.d10',
                    'kind': 'rewrite',
                    'expr': 'NOT (A AND (B OR C))',
                    'vars': ['A', 'B', 'C'],
                    'form': 'no_not_bracket',
                    'text': {'en': 'Open the brackets after <code>NOT</code>: write the same condition without <code>NOT</code> in front of a bracket.',
                             'ru': 'Раскрой скобки после <code>NOT</code>: запиши то же условие без <code>NOT</code> перед скобкой.'},
                    'answer': 'NOT A OR (NOT B AND NOT C)',
                    'explain': {'en': 'Step by step: <code>NOT A OR NOT (B OR C)</code>, then the inner bracket: <code>NOT A OR (NOT B AND NOT C)</code>. The brackets around <code>NOT B AND NOT '
                                      'C</code> are not required (AND goes first), but they make it easier to read.',
                                'ru': 'По шагам: <code>NOT A OR NOT (B OR C)</code>, потом внутренняя скобка: <code>NOT A OR (NOT B AND NOT C)</code>. Скобки вокруг <code>NOT B AND NOT C</code> не '
                                      'обязательны (AND выполняется первым), но с ними легче читать.'}},
                   {'id': 'lg.d11',
                    'kind': 'rewrite',
                    'expr': "NOT (city = 'Paris')",
                    'domain': {'city': ['Paris', 'Berlin', 'London']},
                    'form': 'no_not',
                    'text': {'en': 'Write the same condition <b>without <code>NOT</code></b>: use the opposite operators.',
                             'ru': 'Запиши то же условие <b>без <code>NOT</code></b>: используй противоположные операторы.'},
                    'answer': "city <> 'Paris'",
                    'explain': {'en': "The opposite of <code>=</code> is <code>&lt;&gt;</code>: <code>city &lt;&gt; 'Paris'</code>.",
                                'ru': "Противоположность <code>=</code> — это <code>&lt;&gt;</code>: <code>city &lt;&gt; 'Paris'</code>."}},
                   {'id': 'lg.d12',
                    'kind': 'rewrite',
                    'expr': 'NOT (salary > 55000)',
                    'domain': {'salary': [54999, 55000, 55001]},
                    'form': 'no_not',
                    'text': {'en': 'Write the same condition <b>without <code>NOT</code></b>: use the opposite operators.',
                             'ru': 'Запиши то же условие <b>без <code>NOT</code></b>: используй противоположные операторы.'},
                    'answer': 'salary <= 55000',
                    'explain': {'en': 'The opposite of “greater” is “less <b>or equal</b>”: <code>salary &lt;= 55000</code>. With <code>&lt;</code> a salary of exactly 55000 would be lost.',
                                'ru': 'Противоположность «больше» — «меньше <b>или равно</b>»: <code>salary &lt;= 55000</code>. С <code>&lt;</code> потерялась бы зарплата ровно 55000.'}},
                   {'id': 'lg.d13',
                    'kind': 'rewrite',
                    'expr': "NOT (city = 'Paris' OR city = 'Berlin')",
                    'domain': {'city': ['Paris', 'Berlin', 'London', 'Madrid']},
                    'form': 'no_not',
                    'text': {'en': 'Write the same condition <b>without <code>NOT</code></b>: use the opposite operators.',
                             'ru': 'Запиши то же условие <b>без <code>NOT</code></b>: используй противоположные операторы.'},
                    'answer': "city <> 'Paris' AND city <> 'Berlin'",
                    'explain': {'en': "<code>OR</code> becomes <code>AND</code>, every <code>=</code> becomes <code>&lt;&gt;</code>: <code>city &lt;&gt; 'Paris' AND city &lt;&gt; 'Berlin'</code>. "
                                      'With <code>OR</code> it would be <code>TRUE</code> for everyone.',
                                'ru': "<code>OR</code> становится <code>AND</code>, каждое <code>=</code> — <code>&lt;&gt;</code>: <code>city &lt;&gt; 'Paris' AND city &lt;&gt; 'Berlin'</code>. С "
                                      '<code>OR</code> было бы <code>TRUE</code> у всех.'}},
                   {'id': 'lg.d14',
                    'kind': 'rewrite',
                    'expr': "NOT (department = 'IT' AND salary > 60000)",
                    'domain': {'department': ['IT', 'HR'], 'salary': [59999, 60000, 60001]},
                    'form': 'no_not',
                    'text': {'en': 'Write the same condition <b>without <code>NOT</code></b>: use the opposite operators.',
                             'ru': 'Запиши то же условие <b>без <code>NOT</code></b>: используй противоположные операторы.'},
                    'answer': "department <> 'IT' OR salary <= 60000",
                    'explain': {'en': "<code>AND</code> becomes <code>OR</code>: <code>department &lt;&gt; 'IT' OR salary &lt;= 60000</code>.",
                                'ru': "<code>AND</code> становится <code>OR</code>: <code>department &lt;&gt; 'IT' OR salary &lt;= 60000</code>."}},
                   {'id': 'lg.d15',
                    'kind': 'rewrite',
                    'expr': 'NOT (hire_year < 2017 OR salary >= 68000)',
                    'domain': {'hire_year': [2016, 2017, 2018], 'salary': [67999, 68000, 68001]},
                    'form': 'no_not',
                    'text': {'en': 'Write the same condition <b>without <code>NOT</code></b>: use the opposite operators.',
                             'ru': 'Запиши то же условие <b>без <code>NOT</code></b>: используй противоположные операторы.'},
                    'answer': 'hire_year >= 2017 AND salary < 68000',
                    'explain': {'en': '<code>OR</code> becomes <code>AND</code>, <code>&lt;</code> becomes <code>&gt;=</code>, <code>&gt;=</code> becomes <code>&lt;</code>: <code>hire_year &gt;= '
                                      '2017 AND salary &lt; 68000</code>.',
                                'ru': '<code>OR</code> становится <code>AND</code>, <code>&lt;</code> — <code>&gt;=</code>, <code>&gt;=</code> — <code>&lt;</code>: <code>hire_year &gt;= 2017 AND '
                                      'salary &lt; 68000</code>.'}},
                   {'id': 'lg.d16',
                    'kind': 'rewrite',
                    'expr': "NOT (city = 'London' AND (department = 'IT' OR salary > 60000))",
                    'domain': {'city': ['London', 'Paris'], 'department': ['IT', 'HR'], 'salary': [59999, 60000, 60001]},
                    'form': 'no_not',
                    'text': {'en': 'Write the same condition <b>without <code>NOT</code></b>: use the opposite operators.',
                             'ru': 'Запиши то же условие <b>без <code>NOT</code></b>: используй противоположные операторы.'},
                    'answer': "city <> 'London' OR (department <> 'IT' AND salary <= 60000)",
                    'explain': {'en': "Outer bracket: <code>NOT city = 'London' OR NOT (department = 'IT' OR salary &gt; 60000)</code>. Inner one: <code>city &lt;&gt; 'London' OR (department "
                                      "&lt;&gt; 'IT' AND salary &lt;= 60000)</code>.",
                                'ru': "Внешняя скобка: <code>NOT city = 'London' OR NOT (department = 'IT' OR salary &gt; 60000)</code>. Внутренняя: <code>city &lt;&gt; 'London' OR (department "
                                      "&lt;&gt; 'IT' AND salary &lt;= 60000)</code>."}},
                   {'id': 'lg.34',
                    'kind': 'value',
                    'expr': 'homework AND (sunny OR umbrella)',
                    'given': {'homework': 1, 'sunny': 0, 'umbrella': 0},
                    'text': {'en': 'The homework is done, it is raining and there is no umbrella. Does Rosa go for a walk?',
                             'ru': 'Уроки сделаны, идёт дождь, зонта нет. Пойдёт ли Роза гулять?'},
                    'explain': {'en': '<code>sunny OR umbrella</code> = <code>FALSE OR FALSE</code> = <code>FALSE</code>. <code>TRUE AND FALSE</code> = <code>FALSE</code>: no walk today.',
                                'ru': '<code>sunny OR umbrella</code> = <code>FALSE OR FALSE</code> = <code>FALSE</code>. <code>TRUE AND FALSE</code> = <code>FALSE</code>: сегодня без '
                                      'прогулки.'},
                    'section': {'en': 'H · From words to logic', 'ru': 'H · От слов к логике'},
                    'intro': {'en': '<p>In everyday language we also join conditions with “and”, “or”, “not”. Brackets show what belongs together.</p>\n'
                                    '<p>“Rosa goes for a walk if she has done her homework and it is sunny or she has an umbrella.” What is meant: the homework is a must, and for the '
                                    'weather there are two options. So: <code>homework AND (sunny OR umbrella)</code>.</p>\n'
                                    '<p>Without brackets SQL reads <code>(homework AND sunny) OR umbrella</code>: with an umbrella she could go without doing her homework.</p>\n'
                                    '<p><b>Example:</b> the values are given as columns of a small one-row table.</p>',
                              'ru': '<p>В обычной речи условия тоже соединяют словами «и», «или», «не». Скобки показывают, что к чему относится.</p>\n'
                                    '<p>«Роза идёт гулять, если сделала уроки и светит солнце или у неё есть зонт». Имеется в виду: уроки — обязательно, а для погоды есть два варианта. '
                                    'Значит: <code>homework AND (sunny OR umbrella)</code>.</p>\n'
                                    '<p>Без скобок SQL прочитает <code>(homework AND sunny) OR umbrella</code>: с зонтом можно пойти гулять и без уроков.</p>\n'
                                    '<p><b>Пример:</b> значения заданы столбцами маленькой таблицы из одной строки.</p>'},
                    'example': 'SELECT homework AND (sunny OR umbrella) AS walk\nFROM (SELECT TRUE AS homework, TRUE AS sunny, FALSE AS umbrella);'},
                   {'id': 'lg.35',
                    'kind': 'value',
                    'expr': 'homework AND (sunny OR umbrella)',
                    'given': {'homework': 1, 'sunny': 0, 'umbrella': 1},
                    'text': {'en': 'The homework is done, it is raining, but Rosa has an umbrella. Does she go for a walk?',
                             'ru': 'Уроки сделаны, идёт дождь, но у Розы есть зонт. Пойдёт ли она гулять?'},
                    'explain': {'en': '<code>sunny OR umbrella</code> = <code>FALSE OR TRUE</code> = <code>TRUE</code>. <code>TRUE AND TRUE</code> = <code>TRUE</code>: Rosa goes, with '
                                      'the umbrella.',
                                'ru': '<code>sunny OR umbrella</code> = <code>FALSE OR TRUE</code> = <code>TRUE</code>. <code>TRUE AND TRUE</code> = <code>TRUE</code>: Роза идёт гулять с '
                                      'зонтом.'}},
                   {'id': 'lg.36',
                    'kind': 'value',
                    'expr': 'homework AND sunny OR umbrella',
                    'given': {'homework': 0, 'sunny': 0, 'umbrella': 1},
                    'text': {'en': 'Someone forgot the brackets. The homework is not done, it is raining, but there is an umbrella. What does the condition without brackets say?',
                             'ru': 'Кто-то забыл скобки. Уроки не сделаны, идёт дождь, но есть зонт. Что скажет условие без скобок?'},
                    'explain': {'en': '<code>AND</code> first: <code>FALSE AND FALSE</code> = <code>FALSE</code>. Then <code>FALSE OR TRUE</code> = <code>TRUE</code>: the condition lets '
                                      'Rosa go without homework. That is why the brackets are needed.',
                                'ru': 'Сначала <code>AND</code>: <code>FALSE AND FALSE</code> = <code>FALSE</code>. Потом <code>FALSE OR TRUE</code> = <code>TRUE</code>: условие '
                                      'отпускает Розу гулять без уроков. Вот зачем нужны скобки.'}},
                   {'id': 'lg.37',
                    'kind': 'value',
                    'expr': 'ticket AND NOT late',
                    'given': {'ticket': 1, 'late': 1},
                    'text': {'en': 'Cinema: you can come in if you have a ticket and you are not late. You have a ticket, but you are late. Do you get in?',
                             'ru': 'Кино: пускают, если есть билет и ты не опоздала. Билет есть, но ты опоздала. Пустят?'},
                    'explain': {'en': "<code>NOT late</code> = <code>NOT TRUE</code> = <code>FALSE</code>. <code>TRUE AND FALSE</code> = <code>FALSE</code>: you don't get in.",
                                'ru': '<code>NOT late</code> = <code>NOT TRUE</code> = <code>FALSE</code>. <code>TRUE AND FALSE</code> = <code>FALSE</code>: не пустят.'}},
                   {'id': 'lg.38',
                    'kind': 'truth',
                    'vars': ['homework', 'sunny', 'umbrella'],
                    'cols': ['homework AND (sunny OR umbrella)'],
                    'text': {'en': "Fill in the whole table for Rosa's walk: all 8 situations.", 'ru': 'Заполни всю таблицу для прогулки Розы: все 8 ситуаций.'},
                    'explain': {'en': 'Without homework (the last 4 rows) it is always <code>FALSE</code>. With homework it is <code>FALSE</code> only when there is neither sun nor '
                                      'umbrella.',
                                'ru': 'Без уроков (последние 4 строки) всегда <code>FALSE</code>. С уроками — <code>FALSE</code> только когда нет ни солнца, ни зонта.'}},
                   {'id': 'lg.39',
                    'kind': 'value',
                    'expr': "1 = 1 AND 'Berlin'",
                    'text': {'en': 'What does this expression return?', 'ru': 'Что вернёт это выражение?'},
                    'explain': {'en': "<code>'Berlin'</code> is not a comparison. SQLite turns it into the number 0, that is <code>FALSE</code>. <code>TRUE AND FALSE</code> = "
                                      '<code>FALSE</code>.',
                                'ru': "<code>'Berlin'</code> — это не сравнение. SQLite превращает его в число 0, то есть <code>FALSE</code>. <code>TRUE AND FALSE</code> = "
                                      '<code>FALSE</code>.'},
                    'section': {'en': 'I · Traps: text and NULL', 'ru': 'I · Ловушки: текст и NULL'},
                    'intro': {'en': "<p><b>Text instead of a comparison.</b> When SQLite needs a logical value and gets text, it turns the text into a number: <code>'Berlin'</code> "
                                    "becomes 0, that is <code>FALSE</code>. That is why <code>city = 'Paris' OR 'Berlin'</code> gives no error: it means <code>city = 'Paris' OR "
                                    'FALSE</code>, and Berlin is lost.</p>\n'
                                    '<p><b>NULL is “unknown”.</b> It is the third logical value:</p>\n'
                                    '<ul>\n'
                                    '<li><code>TRUE AND NULL</code> = <code>NULL</code> (it depends on the unknown part), but <code>FALSE AND NULL</code> = <code>FALSE</code> (one '
                                    '<code>FALSE</code> is enough).</li>\n'
                                    '<li><code>TRUE OR NULL</code> = <code>TRUE</code> (one <code>TRUE</code> is enough), but <code>FALSE OR NULL</code> = <code>NULL</code>.</li>\n'
                                    '<li><code>NOT NULL</code> = <code>NULL</code>. Any comparison with <code>NULL</code>, even <code>NULL = NULL</code>, is <code>NULL</code>.</li>\n'
                                    '<li><code>WHERE</code> keeps only <code>TRUE</code> rows, so the rows with <code>NULL</code> are dropped.</li>\n'
                                    '</ul>\n'
                                    '<p><b>Example:</b></p>',
                              'ru': "<p><b>Текст вместо сравнения.</b> Когда SQLite нужно логическое значение, а там текст, он превращает текст в число: <code>'Berlin'</code> становится "
                                    "0, то есть <code>FALSE</code>. Поэтому <code>city = 'Paris' OR 'Berlin'</code> не даёт ошибки: это значит <code>city = 'Paris' OR FALSE</code>, и "
                                    'Берлин теряется.</p>\n'
                                    '<p><b>NULL — это «неизвестно».</b> Третье логическое значение:</p>\n'
                                    '<ul>\n'
                                    '<li><code>TRUE AND NULL</code> = <code>NULL</code> (зависит от неизвестной части), а <code>FALSE AND NULL</code> = <code>FALSE</code> (одного '
                                    '<code>FALSE</code> хватает).</li>\n'
                                    '<li><code>TRUE OR NULL</code> = <code>TRUE</code> (одного <code>TRUE</code> хватает), а <code>FALSE OR NULL</code> = <code>NULL</code>.</li>\n'
                                    '<li><code>NOT NULL</code> = <code>NULL</code>. Любое сравнение с <code>NULL</code>, даже <code>NULL = NULL</code>, даёт <code>NULL</code>.</li>\n'
                                    '<li><code>WHERE</code> оставляет только строки с <code>TRUE</code>, поэтому строки с <code>NULL</code> отбрасываются.</li>\n'
                                    '</ul>\n'
                                    '<p><b>Пример:</b></p>'},
                    'example': "SELECT 1 = 2 OR 'Paris' AS text_trap, FALSE OR NULL AS false_or_null;"},
                   {'id': 'lg.40',
                    'text': {'en': "Show <code>first_name</code>, <code>city</code> and two columns: <code>wrong</code> = <code>city = 'Paris' OR 'Berlin'</code> and <code>right</code> = "
                                   "<code>city = 'Paris' OR city = 'Berlin'</code>. Look at the employees from Berlin.",
                             'ru': "Выведи <code>first_name</code>, <code>city</code> и два столбца: <code>wrong</code> = <code>city = 'Paris' OR 'Berlin'</code> и <code>right</code> = "
                                   "<code>city = 'Paris' OR city = 'Berlin'</code>. Посмотри на сотрудников из Берлина."},
                    'answer': "SELECT first_name, city,\n       city = 'Paris' OR 'Berlin' AS wrong,\n       city = 'Paris' OR city = 'Berlin' AS right\nFROM employees;"},
                   {'id': 'lg.41',
                    'kind': 'value',
                    'expr': 'TRUE AND NULL',
                    'nulls': True,
                    'text': {'en': 'What does this expression return?', 'ru': 'Что вернёт это выражение?'},
                    'explain': {'en': '<code>AND</code> needs to know both sides. The left one is <code>TRUE</code>, so everything depends on the unknown one: <code>NULL</code>.',
                                'ru': '<code>AND</code> нужно знать обе стороны. Левая — <code>TRUE</code>, значит всё зависит от неизвестной: <code>NULL</code>.'}},
                   {'id': 'lg.42',
                    'kind': 'value',
                    'expr': 'FALSE AND NULL',
                    'nulls': True,
                    'text': {'en': 'What does this expression return?', 'ru': 'Что вернёт это выражение?'},
                    'explain': {'en': 'One <code>FALSE</code> is enough for <code>AND</code> to be <code>FALSE</code>, whatever the unknown part is.',
                                'ru': 'Одного <code>FALSE</code> хватает, чтобы <code>AND</code> был <code>FALSE</code>, какой бы ни была неизвестная часть.'}},
                   {'id': 'lg.43',
                    'kind': 'value',
                    'expr': 'TRUE OR NULL',
                    'nulls': True,
                    'text': {'en': 'What does this expression return?', 'ru': 'Что вернёт это выражение?'},
                    'explain': {'en': 'One <code>TRUE</code> is enough for <code>OR</code> to be <code>TRUE</code>, whatever the unknown part is.',
                                'ru': 'Одного <code>TRUE</code> хватает, чтобы <code>OR</code> был <code>TRUE</code>, какой бы ни была неизвестная часть.'}},
                   {'id': 'lg.44',
                    'kind': 'value',
                    'expr': 'NULL = NULL',
                    'nulls': True,
                    'text': {'en': 'What does this expression return?', 'ru': 'Что вернёт это выражение?'},
                    'explain': {'en': 'Two unknown values are not known to be equal, so the answer is unknown too: <code>NULL</code>. To check for <code>NULL</code> use <code>IS '
                                      'NULL</code>: <code>NULL IS NULL</code> is <code>TRUE</code>.',
                                'ru': 'Про два неизвестных значения нельзя сказать, что они равны, поэтому ответ тоже неизвестен: <code>NULL</code>. Чтобы проверить на <code>NULL</code>, '
                                      'используй <code>IS NULL</code>: <code>NULL IS NULL</code> — это <code>TRUE</code>.'}},
                   {'id': 'lg.45',
                    'kind': 'truth',
                    'vars': ['A', 'B'],
                    'cols': ['A AND B'],
                    'nulls': True,
                    'text': {'en': 'Fill in the truth table of <code>AND</code> with <code>NULL</code>: 9 rows.',
                             'ru': 'Заполни таблицу истинности для <code>AND</code> с <code>NULL</code>: 9 строк.'},
                    'explain': {'en': 'Any <code>FALSE</code> gives <code>FALSE</code>. Otherwise, if there is a <code>NULL</code>, the result is <code>NULL</code>.',
                                'ru': 'Любой <code>FALSE</code> даёт <code>FALSE</code>. Иначе, если есть <code>NULL</code>, результат <code>NULL</code>.'}},
                   {'id': 'lg.46',
                    'kind': 'truth',
                    'vars': ['A', 'B'],
                    'cols': ['A OR B'],
                    'nulls': True,
                    'text': {'en': 'Fill in the truth table of <code>OR</code> with <code>NULL</code>.', 'ru': 'Заполни таблицу истинности для <code>OR</code> с <code>NULL</code>.'},
                    'explain': {'en': 'Any <code>TRUE</code> gives <code>TRUE</code>. Otherwise, if there is a <code>NULL</code>, the result is <code>NULL</code>.',
                                'ru': 'Любой <code>TRUE</code> даёт <code>TRUE</code>. Иначе, если есть <code>NULL</code>, результат <code>NULL</code>.'}}]},
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
            "available": True,
            "title": {"en": "ORDER BY & LIMIT", "ru": "ORDER BY и LIMIT"},
            "topics": {"en": "Sorting, top-N queries", "ru": "Сортировка, первые N строк"},
            "theory": {
                "en": """<p><code>ORDER BY</code> sorts the result, like the sort button on an Excel column. <code>LIMIT</code> keeps only the first rows of it.</p>
<pre class="code">SELECT column1, column2
FROM table_name
WHERE condition
ORDER BY column1 [ASC|DESC], column2 [ASC|DESC]
LIMIT n OFFSET m;</pre>
<h4>Sorting</h4>
<ul>
  <li><code>ASC</code> — ascending: 1→9, A→Z, old dates → new. It is the default, so <code>ORDER BY price</code> = <code>ORDER BY price ASC</code>.</li>
  <li><code>DESC</code> — descending: 9→1, Z→A, new dates → old.</li>
  <li>Several columns: the first one is the main sort, the next ones only sort rows that are <b>equal</b> in the previous columns.</li>
  <li>Each column has its own direction: in <code>ORDER BY a DESC, b</code> the column <code>b</code> is ascending.</li>
</ul>
<h4>NULL in sorting</h4>
<ul>
  <li>In our trainer (SQLite) <code>NULL</code> is smaller than any value: <b>first</b> with <code>ASC</code>, <b>last</b> with <code>DESC</code>. MySQL does the same, PostgreSQL and Oracle do the opposite.</li>
  <li><code>NULLS FIRST</code> / <code>NULLS LAST</code> after the direction put <code>NULL</code> where you want.</li>
</ul>
<h4>LIMIT and OFFSET</h4>
<ul>
  <li><code>LIMIT n</code> — only the first <code>n</code> rows.</li>
  <li><code>OFFSET m</code> — skip <code>m</code> rows first. <code>LIMIT 3 OFFSET 3</code> = rows 4, 5, 6.</li>
  <li>Without <code>ORDER BY</code> “the first rows” are any rows. Use <code>LIMIT</code> together with <code>ORDER BY</code>.</li>
</ul>
<h4>The order of work</h4>
<p><code>FROM</code> → <code>WHERE</code> → <code>ORDER BY</code> → <code>LIMIT</code>/<code>OFFSET</code>. <code>LIMIT</code> is always the last step.</p>""",
                "ru": """<p><code>ORDER BY</code> сортирует результат, как кнопка сортировки на столбце в Excel. <code>LIMIT</code> оставляет только первые строки.</p>
<pre class="code">SELECT column1, column2
FROM table_name
WHERE condition
ORDER BY column1 [ASC|DESC], column2 [ASC|DESC]
LIMIT n OFFSET m;</pre>
<h4>Сортировка</h4>
<ul>
  <li><code>ASC</code> — по возрастанию: 1→9, A→Z, старые даты → новые. Это значение по умолчанию: <code>ORDER BY price</code> = <code>ORDER BY price ASC</code>.</li>
  <li><code>DESC</code> — по убыванию: 9→1, Z→A, новые даты → старые.</li>
  <li>Несколько столбцов: первый — главная сортировка, следующие сортируют только строки, у которых предыдущие столбцы <b>равны</b>.</li>
  <li>У каждого столбца своё направление: в <code>ORDER BY a DESC, b</code> столбец <code>b</code> идёт по возрастанию.</li>
</ul>
<h4>NULL при сортировке</h4>
<ul>
  <li>В нашем тренажёре (SQLite) <code>NULL</code> меньше любого значения: <b>в начале</b> при <code>ASC</code> и <b>в конце</b> при <code>DESC</code>. В MySQL так же, в PostgreSQL и Oracle наоборот.</li>
  <li><code>NULLS FIRST</code> / <code>NULLS LAST</code> после направления ставят <code>NULL</code> куда нужно.</li>
</ul>
<h4>LIMIT и OFFSET</h4>
<ul>
  <li><code>LIMIT n</code> — только первые <code>n</code> строк.</li>
  <li><code>OFFSET m</code> — сначала пропустить <code>m</code> строк. <code>LIMIT 3 OFFSET 3</code> = строки 4, 5, 6.</li>
  <li>Без <code>ORDER BY</code> «первые строки» — это какие попало строки. Пиши <code>LIMIT</code> вместе с <code>ORDER BY</code>.</li>
</ul>
<h4>Порядок работы</h4>
<p><code>FROM</code> → <code>WHERE</code> → <code>ORDER BY</code> → <code>LIMIT</code>/<code>OFFSET</code>. <code>LIMIT</code> всегда последний шаг.</p>""",
            },
            "tips": {
                "en": [
                    "<b>Predict before running.</b> In section B ask where the <code>NULL</code> rows will be, then run and compare.",
                    "<b>Swap the keys.</b> In tasks 9–10 swap the two <code>ORDER BY</code> columns and ask what changes before running.",
                    "<b>LIMIT without ORDER BY.</b> In SQLite <code>SELECT * FROM products LIMIT 3;</code> usually returns the first rows of the table, so it looks fine. Explain that it is luck: another database, or the same one after changes, may return other rows.",
                    "<b>OFFSET arithmetic.</b> “Skip 3, take 3” = rows 4, 5, 6. Students often read <code>LIMIT 3 OFFSET 3</code> as “rows 3 to 3”.",
                    "<b>DESC scope.</b> Point at <code>ORDER BY a DESC, b</code> and ask: is <code>b</code> ascending or descending?",
                    "The <b>Explain condition</b> button works only for <code>WHERE</code>; it does not explain sorting.",
                ],
                "ru": [
                    "<b>Предсказание до запуска.</b> В разделе B спрашивай, где окажутся строки с <code>NULL</code>, потом запускай и сравнивайте.",
                    "<b>Поменяй столбцы местами.</b> В задачах 9–10 поменяй два столбца в <code>ORDER BY</code> и спроси, что изменится, до запуска.",
                    "<b>LIMIT без ORDER BY.</b> В SQLite <code>SELECT * FROM products LIMIT 3;</code> обычно возвращает первые строки таблицы, и кажется, что всё правильно. Объясни, что это везение: другая база или эта же после изменений вернёт другие строки.",
                    "<b>Счёт с OFFSET.</b> «Пропусти 3, возьми 3» = строки 4, 5, 6. Часто <code>LIMIT 3 OFFSET 3</code> читают как «строки с 3 по 3».",
                    "<b>DESC действует на один столбец.</b> Покажи <code>ORDER BY a DESC, b</code> и спроси: <code>b</code> по возрастанию или по убыванию?",
                    "Кнопка <b>«Разобрать условие»</b> работает только для <code>WHERE</code>, сортировку она не объясняет.",
                ],
            },
            "tables": ["products", "orders"],
            "seed": """CREATE TABLE products (
    product_id   INTEGER PRIMARY KEY,
    product_name VARCHAR(60) NOT NULL,
    category     VARCHAR(30) NOT NULL,
    price        DECIMAL(8,2),
    stock        INTEGER,
    supplier     VARCHAR(40)
);
INSERT INTO products VALUES
(1,  'Wireless Mouse',      'Electronics', 25.99,  120,  'TechSupply Co'),
(2,  'Mechanical Keyboard', 'Electronics', 89.50,  45,   'TechSupply Co'),
(3,  'USB-C Cable',         'Electronics', 12.00,  300,  'CableWorld'),
(4,  'Monitor Stand',       'Furniture',   45.00,  NULL, 'DeskPro'),
(5,  'Office Chair',        'Furniture',   199.99, 18,   'DeskPro'),
(6,  'Standing Desk',       'Furniture',   349.00, 7,    NULL),
(7,  'Notebook Set',        'Stationery',  8.75,   500,  'PaperPlus'),
(8,  'Gel Pens (12)',       'Stationery',  6.50,   NULL, 'PaperPlus'),
(9,  'Sticky Notes',        'Stationery',  3.25,   800,  'PaperPlus'),
(10, 'Webcam HD',           'Electronics', 59.99,  60,   'TechSupply Co'),
(11, 'Desk Lamp',           'Furniture',   32.50,  25,   'DeskPro'),
(12, 'Highlighter Pack',    'Stationery',  4.99,   0,    NULL);

CREATE TABLE orders (
    order_id    INTEGER PRIMARY KEY,
    product_id  INTEGER NOT NULL,
    customer    VARCHAR(40) NOT NULL,
    quantity    INTEGER NOT NULL,
    order_date  DATE NOT NULL,
    discount    DECIMAL(4,2),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
INSERT INTO orders VALUES
(1,  1,  'Alice', 2,  '2024-01-05', 0.10),
(2,  5,  'Bob',   1,  '2024-01-07', NULL),
(3,  3,  'Alice', 5,  '2024-01-09', 0.05),
(4,  6,  'Carol', 1,  '2024-01-10', NULL),
(5,  2,  'Bob',   2,  '2024-01-12', 0.15),
(6,  9,  'Dave',  10, '2024-01-15', NULL),
(7,  1,  'Carol', 1,  '2024-01-18', 0.00),
(8,  10, 'Alice', 3,  '2024-01-20', 0.20),
(9,  7,  'Dave',  4,  '2024-01-22', NULL),
(10, 11, 'Bob',   2,  '2024-01-25', 0.10),
(11, 3,  'Carol', 12, '2024-01-28', NULL),
(12, 12, 'Dave',  6,  '2024-02-01', 0.25);""",
            "tasks": [
                # Section A
                {"id": "3.1",
                 "section": {"en": "A · Sorting by one column", "ru": "A · Сортировка по одному столбцу"},
                 "intro": {"en": "<p><code>ORDER BY</code> sorts the result. <code>ASC</code> (the default) goes from small to large: 1→9, A→Z, old dates → new. <code>DESC</code> goes the other way. <code>ORDER BY</code> comes after <code>FROM</code> (and after <code>WHERE</code>, if there is one).</p>\n<p>Dates written as <code>'2024-01-05'</code> sort correctly, because the year comes first, then the month, then the day.</p>\n<p><b>Example:</b> orders from the biggest quantity to the smallest.</p>",
                           "ru": "<p><code>ORDER BY</code> сортирует результат. <code>ASC</code> (по умолчанию) — от меньшего к большему: 1→9, A→Z, старые даты → новые. <code>DESC</code> — наоборот. <code>ORDER BY</code> пишется после <code>FROM</code> (и после <code>WHERE</code>, если он есть).</p>\n<p>Даты вида <code>'2024-01-05'</code> сортируются правильно: сначала идёт год, потом месяц, потом день.</p>\n<p><b>Пример:</b> заказы от самого большого количества к самому маленькому.</p>"},
                 "example": "SELECT order_id, customer, quantity\nFROM orders\nORDER BY quantity DESC;",
                 "text": {"en": "Get all products sorted by <code>price</code> from the cheapest to the most expensive.", "ru": "Выведи все товары, отсортированные по <code>price</code> от самого дешёвого к самому дорогому."},
                 "answer": "SELECT * FROM products ORDER BY price ASC;"},
                {"id": "3.2",
                 "text": {"en": "Get all products sorted by <code>price</code> from the most expensive to the cheapest.", "ru": "Выведи все товары, отсортированные по <code>price</code> от самого дорогого к самому дешёвому."},
                 "answer": "SELECT * FROM products ORDER BY price DESC;"},
                {"id": "3.3",
                 "text": {"en": "Get all products sorted alphabetically by <code>product_name</code>.", "ru": "Выведи все товары в алфавитном порядке по <code>product_name</code>."},
                 "answer": "SELECT * FROM products ORDER BY product_name ASC;"},
                {"id": "3.4",
                 "text": {"en": "Get all orders from the newest to the oldest (<code>order_date</code>).", "ru": "Выведи все заказы от самого нового к самому старому (<code>order_date</code>)."},
                 "answer": "SELECT * FROM orders ORDER BY order_date DESC;"},

                # Section B
                {"id": "3.5",
                 "section": {"en": "B · NULL in sorting", "ru": "B · NULL при сортировке"},
                 "intro": {"en": "<p>Where does <code>NULL</code> go? Every database decides for itself. In our trainer (SQLite) <code>NULL</code> counts as <b>smaller than any value</b>: it comes <b>first</b> with <code>ASC</code> and <b>last</b> with <code>DESC</code>. MySQL does the same, PostgreSQL and Oracle do the opposite.</p>\n<p>To choose the place yourself, write <code>NULLS FIRST</code> or <code>NULLS LAST</code> after the direction.</p>\n<p><b>Example:</b> orders from the biggest discount to the smallest, but orders without a discount first.</p>",
                           "ru": "<p>Куда попадает <code>NULL</code>? Каждая база решает сама. В нашем тренажёре (SQLite) <code>NULL</code> считается <b>меньше любого значения</b>: он идёт <b>в начале</b> при <code>ASC</code> и <b>в конце</b> при <code>DESC</code>. В MySQL так же, в PostgreSQL и Oracle наоборот.</p>\n<p>Чтобы выбрать место самой, напиши <code>NULLS FIRST</code> или <code>NULLS LAST</code> после направления.</p>\n<p><b>Пример:</b> заказы от самой большой скидки к самой маленькой, но заказы без скидки — в начале.</p>"},
                 "example": "SELECT order_id, customer, discount\nFROM orders\nORDER BY discount DESC NULLS FIRST;",
                 "text": {"en": "Get all products sorted by <code>supplier</code> from A to Z. Where did the products without a supplier end up?", "ru": "Выведи все товары, отсортированные по <code>supplier</code> от A до Z. Где оказались товары без поставщика?"},
                 "answer": "SELECT * FROM products ORDER BY supplier ASC;"},
                {"id": "3.6",
                 "text": {"en": "Get all products sorted by <code>stock</code> from the smallest to the largest. Which products have no stock data?", "ru": "Выведи все товары, отсортированные по <code>stock</code> от меньшего к большему. У каких товаров нет данных об остатке?"},
                 "answer": "SELECT * FROM products ORDER BY stock ASC;"},
                {"id": "3.7",
                 "text": {"en": "Get all orders sorted by <code>discount</code> from the biggest to the smallest. Where are the orders without a discount now?", "ru": "Выведи все заказы, отсортированные по <code>discount</code> от самой большой скидки к самой маленькой. Где теперь заказы без скидки?"},
                 "answer": "SELECT * FROM orders ORDER BY discount DESC;"},
                {"id": "3.8",
                 "text": {"en": "Get all products sorted by <code>stock</code> from the smallest to the largest, but with the products whose stock is unknown (<code>NULL</code>) at the end.", "ru": "Выведи все товары, отсортированные по <code>stock</code> от меньшего к большему, но товары с неизвестным остатком (<code>NULL</code>) — в конце."},
                 "answer": "SELECT * FROM products ORDER BY stock ASC NULLS LAST;"},

                # Section C
                {"id": "3.9",
                 "section": {"en": "C · Sorting by several columns", "ru": "C · Сортировка по нескольким столбцам"},
                 "intro": {"en": "<p>You can sort by several columns separated by commas. The first column is the main sort. The second one only matters for rows where the first is <b>equal</b>: like a class list sorted by surname, and inside the same surname by first name.</p>\n<p>Each column has its <b>own</b> direction. <code>ORDER BY a DESC, b</code> means <code>a</code> descending but <code>b</code> <b>ascending</b>: <code>DESC</code> covers only the column right before it.</p>\n<p><b>Example:</b> orders by customer, and for each customer from the biggest quantity to the smallest.</p>",
                           "ru": "<p>Сортировать можно по нескольким столбцам через запятую. Первый столбец — главная сортировка. Второй работает только для строк, у которых первый <b>одинаковый</b>: как список класса по фамилии, а при одинаковой фамилии — по имени.</p>\n<p>У каждого столбца <b>своё</b> направление. <code>ORDER BY a DESC, b</code> значит: <code>a</code> по убыванию, а <code>b</code> <b>по возрастанию</b>. <code>DESC</code> действует только на столбец прямо перед ним.</p>\n<p><b>Пример:</b> заказы по покупателю, а у каждого покупателя — от самого большого количества к самому маленькому.</p>"},
                 "example": "SELECT customer, quantity, order_date\nFROM orders\nORDER BY customer ASC, quantity DESC;",
                 "text": {"en": "Get all products sorted by <code>category</code> A→Z, and inside each category by <code>price</code> from the cheapest.", "ru": "Выведи все товары, отсортированные по <code>category</code> от A до Z, а внутри категории — по <code>price</code> от самого дешёвого."},
                 "answer": "SELECT * FROM products ORDER BY category ASC, price ASC;"},
                {"id": "3.10",
                 "text": {"en": "Get all products sorted by <code>category</code> A→Z, and inside each category by <code>price</code> from the most expensive.", "ru": "Выведи все товары, отсортированные по <code>category</code> от A до Z, а внутри категории — по <code>price</code> от самого дорогого."},
                 "answer": "SELECT * FROM products ORDER BY category ASC, price DESC;"},
                {"id": "3.11",
                 "text": {"en": "Get all orders sorted by <code>customer</code> A→Z, and for each customer from the newest order to the oldest.", "ru": "Выведи все заказы, отсортированные по <code>customer</code> от A до Z, а у каждого покупателя — от самого нового заказа к самому старому."},
                 "answer": "SELECT * FROM orders ORDER BY customer ASC, order_date DESC;"},
                {"id": "3.12",
                 "text": {"en": "Get all orders sorted by <code>product_id</code> ascending, and for the same product by <code>quantity</code> descending.", "ru": "Выведи все заказы, отсортированные по <code>product_id</code> по возрастанию, а для одного и того же товара — по <code>quantity</code> по убыванию."},
                 "answer": "SELECT * FROM orders ORDER BY product_id ASC, quantity DESC;"},
                {"id": "3.13",
                 "text": {"en": "Get all products sorted by <code>stock</code> from the largest to the smallest, and with the same stock by <code>product_name</code> A→Z.", "ru": "Выведи все товары, отсортированные по <code>stock</code> от большего к меньшему, а при одинаковом остатке — по <code>product_name</code> от A до Z."},
                 "answer": "SELECT * FROM products ORDER BY stock DESC, product_name ASC;"},
                {"id": "3.14",
                 "text": {"en": "Get all orders sorted by <code>quantity</code> from the largest to the smallest, and with the same quantity from the newest order to the oldest.", "ru": "Выведи все заказы, отсортированные по <code>quantity</code> от большего к меньшему, а при одинаковом количестве — от самого нового заказа к самому старому."},
                 "answer": "SELECT * FROM orders ORDER BY quantity DESC, order_date DESC;"},

                # Section D
                {"id": "3.15",
                 "section": {"en": "D · LIMIT and OFFSET", "ru": "D · LIMIT и OFFSET"},
                 "intro": {"en": "<p><code>LIMIT n</code> keeps only the first <code>n</code> rows of the result. <code>OFFSET m</code> skips <code>m</code> rows first: <code>LIMIT 3 OFFSET 3</code> = skip 3, take 3, so rows 4, 5 and 6.</p>\n<p>“The first rows” only make sense after sorting, so <code>LIMIT</code> almost always goes with <code>ORDER BY</code>. In the query <code>LIMIT</code> comes after <code>ORDER BY</code>, and <code>OFFSET</code> after <code>LIMIT</code>.</p>\n<p><b>Example:</b> the 2 orders with the biggest quantity.</p>",
                           "ru": "<p><code>LIMIT n</code> оставляет только первые <code>n</code> строк результата. <code>OFFSET m</code> сначала пропускает <code>m</code> строк: <code>LIMIT 3 OFFSET 3</code> = пропусти 3, возьми 3, то есть строки 4, 5 и 6.</p>\n<p>«Первые строки» имеют смысл только после сортировки, поэтому <code>LIMIT</code> почти всегда идёт вместе с <code>ORDER BY</code>. В запросе <code>LIMIT</code> пишется после <code>ORDER BY</code>, а <code>OFFSET</code> — после <code>LIMIT</code>.</p>\n<p><b>Пример:</b> 2 заказа с самым большим количеством.</p>"},
                 "example": "SELECT order_id, customer, quantity\nFROM orders\nORDER BY quantity DESC\nLIMIT 2;",
                 "text": {"en": "Get the 3 most expensive products.", "ru": "Выведи 3 самых дорогих товара."},
                 "answer": "SELECT * FROM products ORDER BY price DESC LIMIT 3;"},
                {"id": "3.16",
                 "text": {"en": "Get the 5 cheapest products.", "ru": "Выведи 5 самых дешёвых товаров."},
                 "answer": "SELECT * FROM products ORDER BY price ASC LIMIT 5;"},
                {"id": "3.17",
                 "text": {"en": "Get the 4 newest orders (by <code>order_date</code>).", "ru": "Выведи 4 самых новых заказа (по <code>order_date</code>)."},
                 "answer": "SELECT * FROM orders ORDER BY order_date DESC LIMIT 4;"},
                {"id": "3.18",
                 "text": {"en": "Get the 3 oldest orders.", "ru": "Выведи 3 самых старых заказа."},
                 "answer": "SELECT * FROM orders ORDER BY order_date ASC LIMIT 3;"},
                {"id": "3.19",
                 "text": {"en": "Sort the products alphabetically by <code>product_name</code> and get rows 4 to 6 (skip 3, take 3).", "ru": "Отсортируй товары по <code>product_name</code> в алфавитном порядке и выведи строки с 4-й по 6-ю (пропусти 3, возьми 3)."},
                 "answer": "SELECT * FROM products ORDER BY product_name ASC LIMIT 3 OFFSET 3;"},
                {"id": "3.20",
                 "text": {"en": "Get the 2nd and the 3rd most expensive products.", "ru": "Выведи второй и третий по дороговизне товары."},
                 "answer": "SELECT * FROM products ORDER BY price DESC LIMIT 2 OFFSET 1;"},

                # Section E
                {"id": "3.21",
                 "section": {"en": "E · WHERE + ORDER BY + LIMIT", "ru": "E · WHERE + ORDER BY + LIMIT"},
                 "intro": {"en": "<p>The order of clauses in a query is fixed: <code>SELECT … FROM … WHERE … ORDER BY … LIMIT …</code>. The database works in the same order: <code>WHERE</code> keeps the right rows, <code>ORDER BY</code> sorts them, and <code>LIMIT</code> cuts last.</p>\n<p>So “the top 3 in Electronics” is: keep Electronics → sort → take 3. Not “take the top 3 of all products and keep the Electronics among them”.</p>\n<p><b>Example:</b> Dave's 2 biggest orders.</p>",
                           "ru": "<p>Порядок частей в запросе фиксирован: <code>SELECT … FROM … WHERE … ORDER BY … LIMIT …</code>. База работает в том же порядке: <code>WHERE</code> оставляет нужные строки, <code>ORDER BY</code> их сортирует, а <code>LIMIT</code> отрезает в самом конце.</p>\n<p>Поэтому «топ-3 в Electronics» — это: оставить Electronics → отсортировать → взять 3. А не «взять топ-3 из всех товаров и оставить среди них Electronics».</p>\n<p><b>Пример:</b> 2 самых больших заказа Dave.</p>"},
                 "example": "SELECT order_id, quantity, order_date\nFROM orders\nWHERE customer = 'Dave'\nORDER BY quantity DESC\nLIMIT 2;",
                 "text": {"en": "Get the 3 most expensive products in the <code>'Electronics'</code> category.", "ru": "Выведи 3 самых дорогих товара в категории <code>'Electronics'</code>."},
                 "answer": "SELECT * FROM products WHERE category = 'Electronics' ORDER BY price DESC LIMIT 3;"},
                {"id": "3.22",
                 "text": {"en": "Get the 4 newest orders of the customers whose name starts with <code>'A'</code> or <code>'B'</code>, the newest first.", "ru": "Выведи 4 самых новых заказа покупателей, чьё имя начинается на <code>'A'</code> или <code>'B'</code>, сначала самые новые."},
                 "answer": "SELECT * FROM orders\nWHERE customer LIKE 'A%' OR customer LIKE 'B%'\nORDER BY order_date DESC\nLIMIT 4;"},
                {"id": "3.23",
                 "text": {"en": "Get the 5 cheapest products that are NOT in the <code>'Stationery'</code> category and have a supplier (not <code>NULL</code>).", "ru": "Выведи 5 самых дешёвых товаров НЕ из категории <code>'Stationery'</code>, у которых есть поставщик (не <code>NULL</code>)."},
                 "answer": "SELECT * FROM products\nWHERE category <> 'Stationery'\n  AND supplier IS NOT NULL\nORDER BY price ASC\nLIMIT 5;"},
                {"id": "3.24",
                 "text": {"en": "Get the 3 products with the smallest <code>stock</code>, without the products whose stock is unknown. With the same stock, the more expensive one first.", "ru": "Выведи 3 товара с самым маленьким <code>stock</code>, без товаров с неизвестным остатком. При одинаковом остатке — сначала более дорогой."},
                 "answer": "SELECT * FROM products\nWHERE stock IS NOT NULL\nORDER BY stock ASC, price DESC\nLIMIT 3;"},
                {"id": "3.25",
                 "text": {"en": "Get the 2 most expensive products with <code>stock</code> greater than 10. With the same price, sort by <code>product_name</code> A→Z.", "ru": "Выведи 2 самых дорогих товара, у которых <code>stock</code> больше 10. При одинаковой цене — по <code>product_name</code> от A до Z."},
                 "answer": "SELECT * FROM products\nWHERE stock > 10\nORDER BY price DESC, product_name ASC\nLIMIT 2;"},

                # Section F
                {"id": "3.26",
                 "section": {"en": "F · Common mistakes", "ru": "F · Типичные ошибки"},
                 "intro": {"en": "<p>Four traps:</p>\n<ul>\n<li><b>LIMIT without ORDER BY.</b> <code>SELECT * FROM products LIMIT 3;</code> returns <i>some</i> 3 rows, not the cheapest and not the most expensive. <code>LIMIT</code> decides <i>how many</i> rows, <code>ORDER BY</code> decides <i>which</i>.</li>\n<li><b>DESC covers one column.</b> <code>ORDER BY price DESC, stock</code> = price descending, stock <b>ascending</b>. If both must be descending, write <code>DESC</code> twice.</li>\n<li><b>OFFSET without ORDER BY.</b> “Skip 3” then skips any 3 rows.</li>\n<li><b>LIMIT is the last step.</b> <code>WHERE</code> filters first, then the rows are sorted, then <code>LIMIT</code> cuts.</li>\n</ul>\n<p><b>Example:</b> both columns descending, each with its own <code>DESC</code>.</p>",
                           "ru": "<p>Четыре ловушки:</p>\n<ul>\n<li><b>LIMIT без ORDER BY.</b> <code>SELECT * FROM products LIMIT 3;</code> возвращает <i>какие-то</i> 3 строки, не самые дешёвые и не самые дорогие. <code>LIMIT</code> решает, <i>сколько</i> строк, а <code>ORDER BY</code> — <i>какие</i>.</li>\n<li><b>DESC действует на один столбец.</b> <code>ORDER BY price DESC, stock</code> = цена по убыванию, остаток <b>по возрастанию</b>. Если оба по убыванию, пиши <code>DESC</code> два раза.</li>\n<li><b>OFFSET без ORDER BY.</b> «Пропусти 3» тогда пропускает какие попало 3 строки.</li>\n<li><b>LIMIT — последний шаг.</b> Сначала <code>WHERE</code> фильтрует, потом строки сортируются, и только потом <code>LIMIT</code> отрезает.</li>\n</ul>\n<p><b>Пример:</b> оба столбца по убыванию, у каждого свой <code>DESC</code>.</p>"},
                 "example": "SELECT customer, order_date\nFROM orders\nORDER BY customer DESC, order_date DESC;",
                 "text": {"en": "Get the 3 products with the smallest <code>product_id</code>.", "ru": "Выведи 3 товара с самыми маленькими <code>product_id</code>."},
                 "answer": "SELECT * FROM products ORDER BY product_id ASC LIMIT 3;"},
                {"id": "3.27",
                 "text": {"en": "Someone wrote <code>SELECT * FROM products LIMIT 3;</code> to get the 3 cheapest products. Write the correct query.", "ru": "Кто-то написал <code>SELECT * FROM products LIMIT 3;</code>, чтобы получить 3 самых дешёвых товара. Напиши правильный запрос."},
                 "answer": "SELECT * FROM products ORDER BY price ASC LIMIT 3;"},
                {"id": "3.28",
                 "text": {"en": "Get all products sorted by <code>category</code> descending (Z→A), and inside each category by <code>price</code> ascending.", "ru": "Выведи все товары, отсортированные по <code>category</code> по убыванию (Z→A), а внутри категории — по <code>price</code> по возрастанию."},
                 "answer": "SELECT * FROM products ORDER BY category DESC, price ASC;"},
                {"id": "3.29",
                 "text": {"en": "Get all orders sorted by <code>product_id</code> descending, and for the same product by <code>quantity</code> descending too.", "ru": "Выведи все заказы, отсортированные по <code>product_id</code> по убыванию, а для одного и того же товара — по <code>quantity</code> тоже по убыванию."},
                 "answer": "SELECT * FROM orders ORDER BY product_id DESC, quantity DESC;"},
                {"id": "3.30",
                 "text": {"en": "Get all orders sorted by <code>discount</code> descending, and with the same discount by <code>order_date</code> descending too.", "ru": "Выведи все заказы, отсортированные по <code>discount</code> по убыванию, а при одинаковой скидке — по <code>order_date</code> тоже по убыванию."},
                 "answer": "SELECT * FROM orders ORDER BY discount DESC, order_date DESC;"},
                {"id": "3.31",
                 "text": {"en": "Skip the 4 most expensive products and get the next 2 (the 5th and the 6th most expensive).", "ru": "Пропусти 4 самых дорогих товара и выведи следующие 2 (пятый и шестой по дороговизне)."},
                 "answer": "SELECT * FROM products ORDER BY price DESC LIMIT 2 OFFSET 4;"},
                {"id": "3.32",
                 "text": {"en": "Get the 3 products with the biggest <code>stock</code> among the products that have a supplier.", "ru": "Выведи 3 товара с самым большим <code>stock</code> среди товаров, у которых есть поставщик."},
                 "answer": "SELECT * FROM products\nWHERE supplier IS NOT NULL\nORDER BY stock DESC\nLIMIT 3;"},
                {"id": "3.33",
                 "text": {"en": "Get the 2 oldest orders of the customers whose name starts with <code>'C'</code>.", "ru": "Выведи 2 самых старых заказа покупателей, чьё имя начинается на <code>'C'</code>."},
                 "answer": "SELECT * FROM orders\nWHERE customer LIKE 'C%'\nORDER BY order_date ASC\nLIMIT 2;"},
                {"id": "3.34",
                 "text": {"en": "Get all products sorted by <code>supplier</code> A→Z, and for the same supplier by <code>product_name</code> A→Z.", "ru": "Выведи все товары, отсортированные по <code>supplier</code> от A до Z, а у одного поставщика — по <code>product_name</code> от A до Z."},
                 "answer": "SELECT * FROM products ORDER BY supplier ASC, product_name ASC;"},
                {"id": "3.35",
                 "text": {"en": "Someone wrote <code>SELECT * FROM products ORDER BY category, price DESC LIMIT 5;</code> to get the 5 most expensive products. Write the correct query.", "ru": "Кто-то написал <code>SELECT * FROM products ORDER BY category, price DESC LIMIT 5;</code>, чтобы получить 5 самых дорогих товаров. Напиши правильный запрос."},
                 "answer": "SELECT * FROM products ORDER BY price DESC LIMIT 5;"},
            ],
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
        {'id': 101,
          'track': 'analyst',
          'available': True,
          'title': {'en': 'Warm-up: the shop and business questions', 'ru': 'Разминка: магазин и вопросы бизнеса'},
          'topics': {'en': 'SELECT, WHERE, ORDER BY, LIMIT, calculated columns', 'ru': 'SELECT, WHERE, ORDER BY, LIMIT, вычисляемые столбцы'},
          'check': 'values',
          'theory': {'en': '<p>Welcome to the analyst course. Here you repeat SQL on real business questions about one online shop.</p>\n'
                           '<h4>The data</h4>\n'
                           '<ul>\n'
                           '  <li><code>customers</code> — who our customers are: city, signup date, the channel they came from (organic, ads, referral, social).</li>\n'
                           '  <li><code>products</code> — the catalogue: category, price and cost (what the product costs us).</li>\n'
                           '  <li><code>orders</code> — every order of 2025: customer, date, status (delivered, cancelled, returned), promo code and amount.</li>\n'
                           '  <li><code>order_items</code> — what is inside each order: product, quantity, price.</li>\n'
                           '</ul>\n'
                           '<h4>How the tasks work</h4>\n'
                           '<p>A question comes from a colleague. Decide the table, the rows, the columns and the order yourself. The answer is checked by its values: the column names '
                           'are up to you, but keep the order of the columns from the question.</p>\n'
                           '<h4>SQLite and PostgreSQL</h4>\n'
                           '<p>The trainer runs SQLite. At work you will more likely meet PostgreSQL (or BigQuery, ClickHouse…). Almost everything is the same; where the syntax differs, '
                           'the theory has a blue <b>PostgreSQL</b> note. One difference to remember from the start: PostgreSQL puts <code>NULL</code> <b>last</b> when sorting '
                           '<code>ASC</code>, SQLite puts it first.</p>',
                     'ru': '<p>Добро пожаловать в курс для аналитиков. Здесь ты повторяешь SQL на настоящих вопросах бизнеса про один интернет-магазин.</p>\n'
                           '<h4>Данные</h4>\n'
                           '<ul>\n'
                           '  <li><code>customers</code> — кто наши клиенты: город, дата регистрации, канал, из которого они пришли (organic, ads, referral, social).</li>\n'
                           '  <li><code>products</code> — каталог: категория, цена и себестоимость (во сколько товар обходится нам).</li>\n'
                           '  <li><code>orders</code> — все заказы 2025 года: клиент, дата, статус (delivered, cancelled, returned), промокод и сумма.</li>\n'
                           '  <li><code>order_items</code> — что внутри каждого заказа: товар, количество, цена.</li>\n'
                           '</ul>\n'
                           '<h4>Как устроены задания</h4>\n'
                           '<p>Вопрос приходит от коллеги. Таблицу, строки, столбцы и порядок решай сама. Ответ проверяется по значениям: названия столбцов — на твой выбор, но порядок '
                           'столбцов должен быть как в вопросе.</p>\n'
                           '<h4>SQLite и PostgreSQL</h4>\n'
                           '<p>Тренажёр работает на SQLite. На работе скорее встретится PostgreSQL (или BigQuery, ClickHouse…). Почти всё одинаково; там, где синтаксис отличается, в '
                           'теории есть синяя пометка <b>PostgreSQL</b>. Одно отличие стоит запомнить сразу: PostgreSQL при сортировке <code>ASC</code> ставит <code>NULL</code> <b>в '
                           'конец</b>, а SQLite — в начало.</p>'},
          'tips': {'en': ['Before she writes SQL, ask her to say the four steps aloud: table → rows → columns → order/limit.',
                          'Play the colleague: rephrase a question in other words and see if she finds the same query.',
                          'Task 12 is about integer division: if she gets 0 or 1 everywhere, that is the reason.'],
                   'ru': ['Прежде чем писать SQL, проси её проговорить четыре шага вслух: таблица → строки → столбцы → порядок/лимит.',
                          'Играй роль коллеги: переформулируй вопрос другими словами и посмотри, найдёт ли она тот же запрос.',
                          'Задание 12 — про целочисленное деление: если везде получается 0 или 1, причина в этом.']},
          'tables': ['customers', 'products', 'orders', 'order_items'],
          'seed': SHOP_SEED,
          'seed_ref': 'shop',
          'tasks': [{'id': 'an1.1',
                     'text': {'en': 'The marketing team asks: which customers came to us from <b>ads</b>? Show their name and city.',
                              'ru': 'Маркетинг спрашивает: какие клиенты пришли к нам из <b>рекламы</b> (ads)? Покажи их имя и город.'},
                     'answer': "SELECT name, city FROM customers WHERE channel = 'ads';",
                     'section': {'en': 'A · Meet the shop', 'ru': 'A · Знакомство с магазином'},
                     'intro': {'en': '<p>From now on you work as an analyst of a small online shop. Questions come from colleagues in plain words, and your job is to turn them into a '
                                     'query.</p>\n'
                                     '<p>Read every question in four steps: <b>which table?</b> → <b>which rows?</b> (<code>WHERE</code>) → <b>which columns?</b> → <b>in what order, how '
                                     'many?</b> (<code>ORDER BY</code>, <code>LIMIT</code>).</p>\n'
                                     '<p>The result is checked by its values. Name the columns as you like, but keep them in the order the question asks for.</p>\n'
                                     '<p><b>Example:</b> “Which customers live in Berlin?”</p>',
                               'ru': '<p>Теперь ты аналитик небольшого интернет-магазина. Вопросы приходят от коллег обычными словами, а твоя работа — превратить их в запрос.</p>\n'
                                     '<p>Читай каждый вопрос в четыре шага: <b>какая таблица?</b> → <b>какие строки?</b> (<code>WHERE</code>) → <b>какие столбцы?</b> → <b>в каком '
                                     'порядке, сколько?</b> (<code>ORDER BY</code>, <code>LIMIT</code>).</p>\n'
                                     '<p>Результат проверяется по значениям. Столбцы можно называть как угодно, но порядок должен быть таким, как в вопросе.</p>\n'
                                     '<p><b>Пример:</b> «Какие клиенты живут в Берлине?»</p>'},
                     'example': "SELECT name, channel\nFROM customers\nWHERE city = 'Berlin';"},
                    {'id': 'an1.2',
                     'text': {'en': 'Which products cost more than 100? Show the name and the price, the most expensive first.',
                              'ru': 'Какие товары стоят дороже 100? Покажи название и цену, сначала самые дорогие.'},
                     'answer': 'SELECT name, price FROM products WHERE price > 100 ORDER BY price DESC;'},
                    {'id': 'an1.3',
                     'text': {'en': 'Customer support wants the list of all <b>cancelled</b> orders (all columns).',
                              'ru': 'Поддержке нужен список всех <b>отменённых</b> (cancelled) заказов (все столбцы).'},
                     'answer': "SELECT * FROM orders WHERE status = 'cancelled';"},
                    {'id': 'an1.4',
                     'text': {'en': 'The CEO asks for the 5 biggest orders of the year: order number, date and amount, the biggest first.',
                              'ru': 'Директор просит 5 самых крупных заказов года: номер заказа, дату и сумму, сначала самый крупный.'},
                     'answer': 'SELECT order_id, order_date, amount FROM orders ORDER BY amount DESC LIMIT 5;'},
                    {'id': 'an1.5',
                     'text': {'en': 'Data quality check: which customers have no city filled in? Show the customer id and the name.',
                              'ru': 'Проверка качества данных: у каких клиентов не заполнен город? Покажи id клиента и имя.'},
                     'answer': 'SELECT customer_id, name FROM customers WHERE city IS NULL;'},
                    {'id': 'an1.6',
                     'text': {'en': 'Finance wants all orders of <b>December 2025</b> that were placed with a promo code (any).',
                              'ru': 'Финансам нужны все заказы <b>декабря 2025</b>, сделанные с промокодом (любым).'},
                     'answer': "SELECT * FROM orders WHERE promo_code IS NOT NULL AND order_date BETWEEN '2025-12-01' AND '2025-12-31';",
                     'section': {'en': 'B · Filters in business language', 'ru': 'B · Фильтры на языке бизнеса'},
                     'intro': {'en': '<p>Business questions often hide several conditions in one sentence. Write each one down separately, then join them with <code>AND</code> / '
                                     '<code>OR</code>, and put brackets around every <code>OR</code>.</p>\n'
                                     "<ul><li>“in December” → <code>order_date BETWEEN '2025-12-01' AND '2025-12-31'</code> (dates are text <code>'YYYY-MM-DD'</code>, so they compare "
                                     'correctly);</li>\n'
                                     '<li>“with a promo code” → <code>promo_code IS NOT NULL</code>;</li>\n'
                                     "<li>“from ads or social” → <code>channel IN ('ads', 'social')</code>.</li></ul>\n"
                                     '<p class="pg"><b>PostgreSQL:</b> dates are a real <code>DATE</code> type, but <code>\'2025-12-01\'</code> works the same way. <code>LIKE</code> is '
                                     "case-sensitive: <code>'a%'</code> does not find <i>Anna</i>. For a search without case use <code>ILIKE</code>.</p>\n"
                                     '<p><b>Example:</b> “Delivered orders of the first quarter over 300”.</p>',
                               'ru': '<p>В вопросах бизнеса в одном предложении часто спрятано несколько условий. Выпиши каждое отдельно, потом соедини их через <code>AND</code> / '
                                     '<code>OR</code> и ставь скобки вокруг каждого <code>OR</code>.</p>\n'
                                     "<ul><li>«в декабре» → <code>order_date BETWEEN '2025-12-01' AND '2025-12-31'</code> (даты — это текст <code>'YYYY-MM-DD'</code>, поэтому "
                                     'сравниваются правильно);</li>\n'
                                     '<li>«с промокодом» → <code>promo_code IS NOT NULL</code>;</li>\n'
                                     "<li>«из рекламы или соцсетей» → <code>channel IN ('ads', 'social')</code>.</li></ul>\n"
                                     '<p class="pg"><b>PostgreSQL:</b> даты — настоящий тип <code>DATE</code>, но <code>\'2025-12-01\'</code> работает так же. <code>LIKE</code> различает '
                                     "регистр: <code>'a%'</code> не найдёт <i>Anna</i>. Для поиска без учёта регистра есть <code>ILIKE</code>.</p>\n"
                                     '<p><b>Пример:</b> «Доставленные заказы первого квартала больше 300».</p>'},
                     'example': 'SELECT order_id, order_date, amount\n'
                                'FROM orders\n'
                                "WHERE status = 'delivered'\n"
                                "  AND order_date BETWEEN '2025-01-01' AND '2025-03-31'\n"
                                '  AND amount > 300;'},
                    {'id': 'an1.7',
                     'text': {'en': 'Show the <b>delivered</b> orders over 200 from the second half of the year (July–December): all columns.',
                              'ru': 'Покажи <b>доставленные</b> заказы больше 200 за второе полугодие (июль–декабрь): все столбцы.'},
                     'answer': "SELECT * FROM orders WHERE status = 'delivered' AND amount > 200 AND order_date >= '2025-07-01';"},
                    {'id': 'an1.8',
                     'text': {'en': 'The buyer asks: which products from <b>Electronics</b> or <b>Sport</b> cost less than 100? Show name, category and price.',
                              'ru': 'Закупщик спрашивает: какие товары из <b>Electronics</b> или <b>Sport</b> стоят меньше 100? Покажи название, категорию и цену.'},
                     'answer': "SELECT name, category, price FROM products WHERE (category = 'Electronics' OR category = 'Sport') AND price < 100;"},
                    {'id': 'an1.9',
                     'text': {'en': 'Which customers signed up in 2025 through <b>ads</b> or <b>social</b> networks? Show name, signup date and channel.',
                              'ru': 'Какие клиенты зарегистрировались в 2025 году через <b>рекламу</b> (ads) или <b>соцсети</b> (social)? Покажи имя, дату регистрации и канал.'},
                     'answer': "SELECT name, signup_date, channel FROM customers WHERE signup_date >= '2025-01-01' AND channel IN ('ads', 'social');"},
                    {'id': 'an1.10',
                     'text': {'en': 'Logistics asks for every order that did <b>not</b> reach the customer happily: cancelled or returned. All columns.',
                              'ru': 'Логистика просит все заказы, которые <b>не</b> дошли до клиента благополучно: отменённые или возвращённые. Все столбцы.'},
                     'answer': "SELECT * FROM orders WHERE status <> 'delivered';"},
                    {'id': 'an1.11',
                     'text': {'en': 'For every product show name, price, cost and the <b>margin</b> in money: price minus cost.',
                              'ru': 'Для каждого товара покажи название, цену, себестоимость и <b>маржу</b> в деньгах: цена минус себестоимость.'},
                     'answer': 'SELECT name, price, cost, price - cost AS margin FROM products;',
                     'section': {'en': 'C · Calculated columns', 'ru': 'C · Вычисляемые столбцы'},
                     'intro': {'en': '<p>Analysts constantly calculate new columns: margin, discount, share. In <code>SELECT</code> you can use <code>+ - * /</code> and give the result a '
                                     'name with <code>AS</code>.</p>\n'
                                     '<p><b>Trap:</b> integer ÷ integer in SQLite (and PostgreSQL) is integer: <code>45 / 100</code> = 0. To get a percent, multiply by <code>100.0</code> '
                                     'first: <code>45 * 100.0 / 100</code> = 45.0. <code>ROUND(x, 1)</code> keeps one digit after the point.</p>\n'
                                     '<p class="pg"><b>PostgreSQL:</b> <code>ROUND(x, 1)</code> needs an exact number (<code>numeric</code>). With <code>100.0</code> in the formula it is '
                                     'one, so the query works as is. If <code>x</code> is <code>double precision</code>, write <code>ROUND(x::numeric, 1)</code>.</p>\n'
                                     '<p><b>Example:</b> the price of each product with a 20% Black Friday discount.</p>',
                               'ru': '<p>Аналитики постоянно считают новые столбцы: маржу, скидку, долю. В <code>SELECT</code> можно использовать <code>+ - * /</code> и называть '
                                     'результат через <code>AS</code>.</p>\n'
                                     '<p><b>Ловушка:</b> целое ÷ целое в SQLite (и в PostgreSQL) даёт целое: <code>45 / 100</code> = 0. Чтобы получить процент, сначала умножь на '
                                     '<code>100.0</code>: <code>45 * 100.0 / 100</code> = 45.0. <code>ROUND(x, 1)</code> оставляет одну цифру после точки.</p>\n'
                                     '<p class="pg"><b>PostgreSQL:</b> <code>ROUND(x, 1)</code> нужно точное число (<code>numeric</code>). Если в формуле есть <code>100.0</code>, оно '
                                     'такое и есть, и запрос работает как есть. Если <code>x</code> имеет тип <code>double precision</code>, пиши <code>ROUND(x::numeric, 1)</code>.</p>\n'
                                     '<p><b>Пример:</b> цена каждого товара со скидкой 20% в Чёрную пятницу.</p>'},
                     'example': 'SELECT name, price, price * 0.8 AS black_friday_price\nFROM products;'},
                    {'id': 'an1.12',
                     'text': {'en': "Show each product's name and its margin as a <b>percent of the price</b>, rounded to 1 decimal, the highest margin first.",
                              'ru': 'Покажи название каждого товара и его маржу в <b>процентах от цены</b>, округлённую до 1 знака, сначала самая высокая.'},
                     'answer': 'SELECT name, ROUND((price - cost) * 100.0 / price, 1) AS margin_pct FROM products ORDER BY margin_pct DESC;'},
                    {'id': 'an1.13',
                     'text': {'en': 'Which products earn us less than 50% margin? Show the name, price and cost.',
                              'ru': 'На каких товарах маржа меньше 50%? Покажи название, цену и себестоимость.'},
                     'answer': 'SELECT name, price, cost FROM products WHERE (price - cost) * 100.0 / price < 50;'},
                    {'id': 'an1.14',
                     'text': {'en': 'A manager is calling customer number 18. Show her 3 most recent orders: order number, date, status and amount.',
                              'ru': 'Менеджер звонит клиентке номер 18. Покажи её 3 последних заказа: номер, дату, статус и сумму.'},
                     'answer': 'SELECT order_id, order_date, status, amount FROM orders WHERE customer_id = 18 ORDER BY order_date DESC LIMIT 3;'},
                    {'id': 'an1.15',
                     'text': {'en': 'Which promo codes have customers actually used? Show each code once.',
                              'ru': 'Какие промокоды клиенты реально использовали? Покажи каждый код один раз.'},
                     'answer': 'SELECT DISTINCT promo_code FROM orders WHERE promo_code IS NOT NULL;'}]},
         {'id': 102,
          'track': 'analyst',
          'available': True,
          'title': {'en': 'Totals and averages', 'ru': 'Итоги и средние'},
          'topics': {'en': 'COUNT, SUM, AVG, MIN, MAX, DISTINCT, shares', 'ru': 'COUNT, SUM, AVG, MIN, MAX, DISTINCT, доли'},
          'check': 'values',
          'theory': {'en': '<p>Most business questions are about <b>one number</b>: how many, how much, what is the average. That is what aggregate functions do.</p>\n'
                           '<table class="ops"><thead><tr><th>Function</th><th>Meaning</th><th>Excel</th></tr></thead><tbody>\n'
                           '<tr><td><code>COUNT(*)</code></td><td>number of rows</td><td>COUNTA</td></tr>\n'
                           '<tr><td><code>COUNT(DISTINCT x)</code></td><td>number of different values</td><td>—</td></tr>\n'
                           '<tr><td><code>SUM(x)</code></td><td>total</td><td>SUM</td></tr>\n'
                           '<tr><td><code>AVG(x)</code></td><td>average</td><td>AVERAGE</td></tr>\n'
                           '<tr><td><code>MIN(x)</code> / <code>MAX(x)</code></td><td>smallest / largest</td><td>MIN / MAX</td></tr>\n'
                           '</tbody></table>\n'
                           '<p>All of them skip <code>NULL</code> (except <code>COUNT(*)</code>, which counts rows). <code>WHERE</code> filters the rows before they are counted.</p>',
                     'ru': '<p>Большинство вопросов бизнеса — про <b>одно число</b>: сколько, на какую сумму, какое среднее. Это и делают агрегатные функции.</p>\n'
                           '<table class="ops"><thead><tr><th>Функция</th><th>Смысл</th><th>Excel</th></tr></thead><tbody>\n'
                           '<tr><td><code>COUNT(*)</code></td><td>число строк</td><td>СЧЁТЗ</td></tr>\n'
                           '<tr><td><code>COUNT(DISTINCT x)</code></td><td>число разных значений</td><td>—</td></tr>\n'
                           '<tr><td><code>SUM(x)</code></td><td>сумма</td><td>СУММ</td></tr>\n'
                           '<tr><td><code>AVG(x)</code></td><td>среднее</td><td>СРЗНАЧ</td></tr>\n'
                           '<tr><td><code>MIN(x)</code> / <code>MAX(x)</code></td><td>минимум / максимум</td><td>МИН / МАКС</td></tr>\n'
                           '</tbody></table>\n'
                           '<p>Все они пропускают <code>NULL</code> (кроме <code>COUNT(*)</code>, который считает строки). <code>WHERE</code> отбирает строки до подсчёта.</p>'},
          'tips': {'en': ['Ask “what number do you expect, roughly?” before running: analysts must notice when a result looks wrong.',
                          'COUNT(*) vs COUNT(column) vs COUNT(DISTINCT column): let her run all three on the same column and explain the difference.',
                          'Revenue = delivered orders only. This rule comes back in every lesson.'],
                   'ru': ['Перед запуском спрашивай «какое число примерно ожидаешь?»: аналитик должен замечать, когда результат выглядит неправдоподобно.',
                          'COUNT(*), COUNT(столбец) и COUNT(DISTINCT столбец): пусть запустит все три на одном столбце и объяснит разницу.',
                          'Выручка = только доставленные заказы. Это правило будет в каждом уроке.']},
          'tables': ['customers', 'products', 'orders', 'order_items'],
          'seed': SHOP_SEED,
          'seed_ref': 'shop',
          'tasks': [{'id': 'an2.1',
                     'text': {'en': 'How many customers do we have?', 'ru': 'Сколько у нас клиентов?'},
                     'answer': 'SELECT COUNT(*) FROM customers;',
                     'section': {'en': 'A · How many? COUNT', 'ru': 'A · Сколько? COUNT'},
                     'intro': {'en': '<p>An <b>aggregate function</b> turns many rows into one number, like the sum in the Excel status bar when you select a column.</p>\n'
                                     '<ul><li><code>COUNT(*)</code> — how many rows;</li>\n'
                                     '<li><code>COUNT(column)</code> — how many rows where the column is <b>not</b> <code>NULL</code>;</li>\n'
                                     '<li><code>COUNT(DISTINCT column)</code> — how many <b>different</b> values.</li></ul>\n'
                                     "<p><code>WHERE</code> works first, so <code>SELECT COUNT(*) FROM orders WHERE status = 'delivered'</code> counts only delivered orders.</p>\n"
                                     '<p><b>Example:</b> all three kinds of COUNT on one column.</p>',
                               'ru': '<p><b>Агрегатная функция</b> превращает много строк в одно число, как сумма в строке состояния Excel, когда выделяешь столбец.</p>\n'
                                     '<ul><li><code>COUNT(*)</code> — сколько строк;</li>\n'
                                     '<li><code>COUNT(column)</code> — в скольких строках столбец <b>не</b> <code>NULL</code>;</li>\n'
                                     '<li><code>COUNT(DISTINCT column)</code> — сколько <b>разных</b> значений.</li></ul>\n'
                                     "<p><code>WHERE</code> работает раньше, поэтому <code>SELECT COUNT(*) FROM orders WHERE status = 'delivered'</code> считает только доставленные "
                                     'заказы.</p>\n'
                                     '<p><b>Пример:</b> все три вида COUNT на одном столбце.</p>'},
                     'example': 'SELECT COUNT(*) AS all_rows,\n       COUNT(city) AS with_city,\n       COUNT(DISTINCT city) AS cities\nFROM customers;'},
                    {'id': 'an2.2',
                     'text': {'en': 'How many orders were <b>delivered</b>?', 'ru': 'Сколько заказов было <b>доставлено</b>?'},
                     'answer': "SELECT COUNT(*) FROM orders WHERE status = 'delivered';"},
                    {'id': 'an2.3',
                     'text': {'en': 'How many orders were placed with a promo code?', 'ru': 'Сколько заказов сделано с промокодом?'},
                     'answer': 'SELECT COUNT(promo_code) FROM orders;'},
                    {'id': 'an2.4',
                     'text': {'en': 'How many <b>different</b> customers have placed at least one order?', 'ru': 'Сколько <b>разных</b> клиентов сделали хотя бы один заказ?'},
                     'answer': 'SELECT COUNT(DISTINCT customer_id) FROM orders;'},
                    {'id': 'an2.5',
                     'text': {'en': 'In how many different cities do our customers live? (An unknown city is not a city.)',
                              'ru': 'В скольких разных городах живут наши клиенты? (Неизвестный город — не город.)'},
                     'answer': 'SELECT COUNT(DISTINCT city) FROM customers;'},
                    {'id': 'an2.6',
                     'text': {'en': 'What is our <b>revenue</b>: the total amount of the delivered orders?', 'ru': 'Какая у нас <b>выручка</b>: общая сумма доставленных заказов?'},
                     'answer': "SELECT SUM(amount) FROM orders WHERE status = 'delivered';",
                     'section': {'en': 'B · How much? SUM and AVG', 'ru': 'B · Сколько денег? SUM и AVG'},
                     'intro': {'en': '<p><code>SUM(column)</code> adds the values up, <code>AVG(column)</code> gives the average. Both skip <code>NULL</code>.</p>\n'
                                     '<p><b>Revenue</b> usually means the money of <b>delivered</b> orders only: cancelled and returned orders bring nothing. The average amount of an '
                                     'order is called the <b>average check</b> (AOV).</p>\n'
                                     '<p><b>Example:</b> the total and the average amount of all cancelled orders.</p>',
                               'ru': '<p><code>SUM(column)</code> складывает значения, <code>AVG(column)</code> даёт среднее. Обе пропускают <code>NULL</code>.</p>\n'
                                     '<p><b>Выручка</b> обычно — это деньги только <b>доставленных</b> заказов: отменённые и возвращённые ничего не приносят. Средняя сумма заказа '
                                     'называется <b>средним чеком</b>.</p>\n'
                                     '<p><b>Пример:</b> общая и средняя сумма всех отменённых заказов.</p>'},
                     'example': "SELECT SUM(amount) AS total, AVG(amount) AS average\nFROM orders\nWHERE status = 'cancelled';"},
                    {'id': 'an2.7',
                     'text': {'en': 'What is the <b>average check</b> of delivered orders? Round it to 2 decimals.',
                              'ru': 'Какой <b>средний чек</b> у доставленных заказов? Округли до 2 знаков.'},
                     'answer': "SELECT ROUND(AVG(amount), 2) FROM orders WHERE status = 'delivered';"},
                    {'id': 'an2.8',
                     'text': {'en': 'What was the revenue of the <b>fourth quarter</b> (October–December)?', 'ru': 'Какой была выручка в <b>четвёртом квартале</b> (октябрь–декабрь)?'},
                     'answer': "SELECT SUM(amount) FROM orders WHERE status = 'delivered' AND order_date >= '2025-10-01';"},
                    {'id': 'an2.9',
                     'text': {'en': 'How much money did we lose on cancelled and returned orders?', 'ru': 'Сколько денег мы потеряли на отменённых и возвращённых заказах?'},
                     'answer': "SELECT SUM(amount) FROM orders WHERE status IN ('cancelled', 'returned');"},
                    {'id': 'an2.10',
                     'text': {'en': 'The warehouse asks: how many product units were ordered in total (all orders)?',
                              'ru': 'Склад спрашивает: сколько единиц товара было заказано всего (во всех заказах)?'},
                     'answer': 'SELECT SUM(quantity) FROM order_items;'},
                    {'id': 'an2.11',
                     'text': {'en': 'Show the biggest and the smallest <b>delivered</b> order amount: two numbers.',
                              'ru': 'Покажи самую большую и самую маленькую сумму <b>доставленного</b> заказа: два числа.'},
                     'answer': "SELECT MAX(amount), MIN(amount) FROM orders WHERE status = 'delivered';",
                     'section': {'en': 'C · Extremes: MIN and MAX', 'ru': 'C · Крайние значения: MIN и MAX'},
                     'intro': {'en': '<p><code>MIN</code> and <code>MAX</code> work for numbers, texts (alphabetically) and dates (the earliest and the latest).</p>\n'
                                     '<p>One query can return several aggregates at once: <code>SELECT MIN(price), MAX(price) FROM products</code>.</p>\n'
                                     '<p><b>Example:</b> when did the first and the last customer sign up?</p>',
                               'ru': '<p><code>MIN</code> и <code>MAX</code> работают с числами, текстом (по алфавиту) и датами (самая ранняя и самая поздняя).</p>\n'
                                     '<p>Один запрос может вернуть несколько агрегатов сразу: <code>SELECT MIN(price), MAX(price) FROM products</code>.</p>\n'
                                     '<p><b>Пример:</b> когда зарегистрировались первый и последний клиенты?</p>'},
                     'example': 'SELECT MIN(signup_date) AS first_signup,\n       MAX(signup_date) AS last_signup\nFROM customers;'},
                    {'id': 'an2.12',
                     'text': {'en': 'When was the first order of the year placed, and when the last one?', 'ru': 'Когда был сделан первый заказ года, а когда последний?'},
                     'answer': 'SELECT MIN(order_date), MAX(order_date) FROM orders;'},
                    {'id': 'an2.13',
                     'text': {'en': 'For the price list: the cheapest price, the most expensive price and the average price (rounded to 2 decimals).',
                              'ru': 'Для прайс-листа: самая низкая цена, самая высокая и средняя (округлённая до 2 знаков).'},
                     'answer': 'SELECT MIN(price), MAX(price), ROUND(AVG(price), 2) FROM products;'},
                    {'id': 'an2.14',
                     'text': {'en': 'A one-line report on delivered orders: number of orders, number of different customers, revenue and the average check (rounded to 2 decimals).',
                              'ru': 'Отчёт в одну строку по доставленным заказам: число заказов, число разных клиентов, выручка и средний чек (округлённый до 2 знаков).'},
                     'answer': "SELECT COUNT(*), COUNT(DISTINCT customer_id), SUM(amount), ROUND(AVG(amount), 2) FROM orders WHERE status = 'delivered';",
                     'section': {'en': 'D · A small report', 'ru': 'D · Маленький отчёт'},
                     'intro': {'en': '<p>A real report is several numbers next to each other. Put all the aggregates into one <code>SELECT</code>.</p>\n'
                                     '<p>A <b>share</b> (percent) is “how many of them” ÷ “how many in total” × 100. A comparison is 1 or 0 (remember the logic lesson), so '
                                     "<code>SUM(status = 'returned')</code> counts the returned orders, and <code>AVG(status = 'returned')</code> is directly their share.</p>\n"
                                     '<p class="pg"><b>PostgreSQL:</b> a comparison is a real <code>boolean</code>, not 1/0, so <code>SUM(status = \'returned\')</code> gives an error. '
                                     "Write <code>COUNT(*) FILTER (WHERE status = 'returned')</code> or <code>SUM(CASE WHEN status = 'returned' THEN 1 ELSE 0 END)</code>. Both also work "
                                     'in SQLite, so they are the safe habit.</p>\n'
                                     '<p><b>Example:</b> the share of orders with a promo code, in percent.</p>',
                               'ru': '<p>Настоящий отчёт — это несколько чисел рядом. Помести все агрегаты в один <code>SELECT</code>.</p>\n'
                                     '<p><b>Доля</b> (процент) — это «сколько таких» ÷ «сколько всего» × 100. Сравнение — это 1 или 0 (вспомни урок логики), поэтому <code>SUM(status = '
                                     "'returned')</code> считает возвращённые заказы, а <code>AVG(status = 'returned')</code> — это сразу их доля.</p>\n"
                                     '<p class="pg"><b>PostgreSQL:</b> сравнение — настоящий <code>boolean</code>, а не 1/0, поэтому <code>SUM(status = \'returned\')</code> даст ошибку. '
                                     "Пиши <code>COUNT(*) FILTER (WHERE status = 'returned')</code> или <code>SUM(CASE WHEN status = 'returned' THEN 1 ELSE 0 END)</code>. Оба варианта "
                                     'работают и в SQLite, так что это надёжная привычка.</p>\n'
                                     '<p><b>Пример:</b> доля заказов с промокодом в процентах.</p>'},
                     'example': 'SELECT ROUND(COUNT(promo_code) * 100.0 / COUNT(*), 1) AS promo_share_pct\nFROM orders;'},
                    {'id': 'an2.15',
                     'text': {'en': 'What percent of all orders were <b>cancelled</b>? Round to 1 decimal.', 'ru': 'Какой процент всех заказов был <b>отменён</b>? Округли до 1 знака.'},
                     'answer': "SELECT ROUND(SUM(status = 'cancelled') * 100.0 / COUNT(*), 1) FROM orders;"},
                    {'id': 'an2.16',
                     'text': {'en': 'What is the average margin of our products in money (price minus cost), rounded to 2 decimals?',
                              'ru': 'Какая средняя маржа наших товаров в деньгах (цена минус себестоимость), с округлением до 2 знаков?'},
                     'answer': 'SELECT ROUND(AVG(price - cost), 2) FROM products;'}]},
         {'id': 103,
          'track': 'analyst',
          'available': True,
          'title': {'en': 'Pivot tables: GROUP BY and HAVING', 'ru': 'Сводные таблицы: GROUP BY и HAVING'},
          'topics': {'en': 'Groups, top lists, filters on groups, months', 'ru': 'Группы, топы, фильтры по группам, месяцы'},
          'check': 'values',
          'theory': {'en': '<p><code>GROUP BY</code> turns one number into a <b>pivot table</b>: the same aggregate, but for every group.</p>\n'
                           '<pre class="code">SELECT column, AGGREGATE(...)\n'
                           'FROM table\n'
                           'WHERE row_condition\n'
                           'GROUP BY column\n'
                           'HAVING group_condition\n'
                           'ORDER BY ...\n'
                           'LIMIT n;</pre>\n'
                           '<ul>\n'
                           '  <li>Every column in <code>SELECT</code> is in <code>GROUP BY</code> or inside an aggregate.</li>\n'
                           '  <li><code>WHERE</code> filters rows before grouping, <code>HAVING</code> filters groups after it.</li>\n'
                           "  <li>The month of a date: <code>strftime('%Y-%m', date)</code> (PostgreSQL: <code>to_char(date, 'YYYY-MM')</code>).</li>\n"
                           '</ul>',
                     'ru': '<p><code>GROUP BY</code> превращает одно число в <b>сводную таблицу</b>: тот же агрегат, но для каждой группы.</p>\n'
                           '<pre class="code">SELECT column, AGGREGATE(...)\n'
                           'FROM table\n'
                           'WHERE row_condition\n'
                           'GROUP BY column\n'
                           'HAVING group_condition\n'
                           'ORDER BY ...\n'
                           'LIMIT n;</pre>\n'
                           '<ul>\n'
                           '  <li>Каждый столбец в <code>SELECT</code> либо в <code>GROUP BY</code>, либо внутри агрегата.</li>\n'
                           '  <li><code>WHERE</code> фильтрует строки до группировки, <code>HAVING</code> — группы после.</li>\n'
                           "  <li>Месяц даты: <code>strftime('%Y-%m', date)</code> (PostgreSQL: <code>to_char(date, 'YYYY-MM')</code>).</li>\n"
                           '</ul>'},
          'tips': {'en': ['Draw the pivot table on paper first: what are the rows, what is in the cells?',
                          'WHERE vs HAVING: ask “is this a condition on one order or on the whole customer?”',
                          'Check the totals: the sum over all groups must equal the number from the aggregates lesson.'],
                   'ru': ['Сначала нарисуйте сводную таблицу на бумаге: что в строках, что в клетках?',
                          'WHERE или HAVING: спрашивай «это условие про один заказ или про клиента целиком?»',
                          'Проверяйте итоги: сумма по всем группам должна совпасть с числом из урока про агрегаты.']},
          'tables': ['customers', 'products', 'orders', 'order_items'],
          'seed': SHOP_SEED,
          'seed_ref': 'shop',
          'tasks': [{'id': 'an3.1',
                     'text': {'en': 'How many customers came from each channel? Show the channel and the number of customers.',
                              'ru': 'Сколько клиентов пришло из каждого канала? Покажи канал и число клиентов.'},
                     'answer': 'SELECT channel, COUNT(*) FROM customers GROUP BY channel;',
                     'section': {'en': 'A · Pivot tables', 'ru': 'A · Сводные таблицы'},
                     'intro': {'en': '<p><code>GROUP BY</code> is a <b>pivot table</b>: the rows are the groups (one per value of the column), and the aggregate is counted inside each '
                                     'group.</p>\n'
                                     '<pre class="code">SELECT status, COUNT(*)      -- one row per status\n'
                                     'FROM orders\n'
                                     'GROUP BY status;</pre>\n'
                                     '<p>The rule: every column in <code>SELECT</code> is either in <code>GROUP BY</code> or inside an aggregate. <code>NULL</code> forms its own '
                                     'group.</p>\n'
                                     '<p class="pg"><b>PostgreSQL:</b> the rule is strict: a column that is neither in <code>GROUP BY</code> nor inside an aggregate is an error. SQLite '
                                     'does not complain and puts some random value of the group there, so keep the rule here too.</p>\n'
                                     '<p><b>Example:</b> how many products in each category, and the most expensive one.</p>',
                               'ru': '<p><code>GROUP BY</code> — это <b>сводная таблица</b>: строки — это группы (по одной на каждое значение столбца), а агрегат считается внутри каждой '
                                     'группы.</p>\n'
                                     '<pre class="code">SELECT status, COUNT(*)      -- одна строка на статус\n'
                                     'FROM orders\n'
                                     'GROUP BY status;</pre>\n'
                                     '<p>Правило: каждый столбец в <code>SELECT</code> либо есть в <code>GROUP BY</code>, либо внутри агрегата. <code>NULL</code> образует свою '
                                     'группу.</p>\n'
                                     '<p class="pg"><b>PostgreSQL:</b> правило строгое: столбец, которого нет ни в <code>GROUP BY</code>, ни внутри агрегата, — это ошибка. SQLite не '
                                     'ругается и подставляет туда случайное значение из группы, поэтому соблюдай правило и здесь.</p>\n'
                                     '<p><b>Пример:</b> сколько товаров в каждой категории и самая высокая цена.</p>'},
                     'example': 'SELECT category, COUNT(*) AS products, MAX(price) AS max_price\nFROM products\nGROUP BY category;'},
                    {'id': 'an3.2',
                     'text': {'en': 'How many orders are there in each status?', 'ru': 'Сколько заказов в каждом статусе?'},
                     'answer': 'SELECT status, COUNT(*) FROM orders GROUP BY status;'},
                    {'id': 'an3.3',
                     'text': {'en': 'For each category: the number of products and the average price (rounded to 2 decimals).',
                              'ru': 'Для каждой категории: число товаров и средняя цена (округлённая до 2 знаков).'},
                     'answer': 'SELECT category, COUNT(*), ROUND(AVG(price), 2) FROM products GROUP BY category;'},
                    {'id': 'an3.4',
                     'text': {'en': 'Revenue of delivered orders by promo code (orders without a code are a group too).',
                              'ru': 'Выручка доставленных заказов по промокодам (заказы без кода — тоже группа).'},
                     'answer': "SELECT promo_code, SUM(amount) FROM orders WHERE status = 'delivered' GROUP BY promo_code;"},
                    {'id': 'an3.5',
                     'text': {'en': 'Where do our customers live? Number of customers per city, the biggest city first.',
                              'ru': 'Где живут наши клиенты? Число клиентов по городам, сначала самый большой город.'},
                     'answer': 'SELECT city, COUNT(*) AS customers FROM customers GROUP BY city ORDER BY customers DESC;'},
                    {'id': 'an3.6',
                     'text': {'en': 'Who are our top 5 customers by revenue? Show customer id and revenue (delivered orders), the biggest first.',
                              'ru': 'Кто наши топ-5 клиентов по выручке? Покажи id клиента и выручку (доставленные заказы), сначала самый крупный.'},
                     'answer': "SELECT customer_id, SUM(amount) AS revenue FROM orders WHERE status = 'delivered' GROUP BY customer_id ORDER BY revenue DESC LIMIT 5;",
                     'section': {'en': 'B · Groups with filters and top lists', 'ru': 'B · Группы с фильтрами и топы'},
                     'intro': {'en': '<p>The order of work: <code>FROM</code> → <code>WHERE</code> (rows) → <code>GROUP BY</code> → aggregates → <code>ORDER BY</code> → '
                                     '<code>LIMIT</code>.</p>\n'
                                     '<p>So <code>WHERE</code> chooses which rows go into the pivot table, and <code>ORDER BY</code> + <code>LIMIT</code> make a “top N” from the finished '
                                     'groups. You can sort by the name of an aggregate: <code>ORDER BY revenue DESC</code>.</p>\n'
                                     '<p><b>Example:</b> the 3 cities with the most customers from ads.</p>',
                               'ru': '<p>Порядок работы: <code>FROM</code> → <code>WHERE</code> (строки) → <code>GROUP BY</code> → агрегаты → <code>ORDER BY</code> → '
                                     '<code>LIMIT</code>.</p>\n'
                                     '<p>То есть <code>WHERE</code> выбирает, какие строки попадут в сводную таблицу, а <code>ORDER BY</code> + <code>LIMIT</code> делают «топ N» из '
                                     'готовых групп. Сортировать можно по имени агрегата: <code>ORDER BY revenue DESC</code>.</p>\n'
                                     '<p><b>Пример:</b> 3 города, где больше всего клиентов из рекламы.</p>'},
                     'example': "SELECT city, COUNT(*) AS customers\nFROM customers\nWHERE channel = 'ads'\nGROUP BY city\nORDER BY customers DESC\nLIMIT 3;"},
                    {'id': 'an3.7',
                     'text': {'en': 'How many orders did each customer place (any status)? Customer id and number of orders, the most active first.',
                              'ru': 'Сколько заказов сделал каждый клиент (любой статус)? Id клиента и число заказов, сначала самые активные.'},
                     'answer': 'SELECT customer_id, COUNT(*) AS orders FROM orders GROUP BY customer_id ORDER BY orders DESC;'},
                    {'id': 'an3.8',
                     'text': {'en': 'The warehouse wants the 3 best-selling products: product id and the total units ordered.',
                              'ru': 'Склад хочет 3 самых продаваемых товара: id товара и общее число заказанных единиц.'},
                     'answer': 'SELECT product_id, SUM(quantity) AS units FROM order_items GROUP BY product_id ORDER BY units DESC LIMIT 3;'},
                    {'id': 'an3.9',
                     'text': {'en': 'Do promo codes change the average check? Average check of delivered orders with a code and without (rounded to 2). Hint: group by <code>promo_code IS '
                                    'NULL</code>.',
                              'ru': 'Меняют ли промокоды средний чек? Средний чек доставленных заказов с промокодом и без (округлённый до 2). Подсказка: группируй по <code>promo_code IS '
                                    'NULL</code>.'},
                     'answer': "SELECT promo_code IS NULL AS no_promo, ROUND(AVG(amount), 2) FROM orders WHERE status = 'delivered' GROUP BY promo_code IS NULL;"},
                    {'id': 'an3.10',
                     'text': {'en': 'Which customers placed <b>more than 3</b> orders? Customer id and number of orders.',
                              'ru': 'Какие клиенты сделали <b>больше 3</b> заказов? Id клиента и число заказов.'},
                     'answer': 'SELECT customer_id, COUNT(*) FROM orders GROUP BY customer_id HAVING COUNT(*) > 3;',
                     'section': {'en': 'C · HAVING: filters on groups', 'ru': 'C · HAVING: фильтр по группам'},
                     'intro': {'en': '<p><code>WHERE</code> filters <b>rows before</b> grouping. <code>HAVING</code> filters <b>groups after</b> grouping, so it can use aggregates: '
                                     '<code>HAVING COUNT(*) &gt; 3</code>.</p>\n'
                                     '<p>“Customers with revenue over 500” is <code>HAVING SUM(amount) &gt; 500</code>. “Delivered orders” is still <code>WHERE status = '
                                     "'delivered'</code>. Many questions need both.</p>\n"
                                     '<p class="pg"><b>PostgreSQL:</b> <code>HAVING</code> cannot use a column\'s alias: write <code>HAVING SUM(amount) &gt; 500</code>, not <code>HAVING '
                                     'revenue &gt; 500</code>. (SQLite allows the alias.) In <code>ORDER BY</code> the alias works in both.</p>\n'
                                     '<p><b>Example:</b> categories with at least 4 products.</p>',
                               'ru': '<p><code>WHERE</code> фильтрует <b>строки до</b> группировки. <code>HAVING</code> фильтрует <b>группы после</b> группировки, поэтому в нём можно '
                                     'использовать агрегаты: <code>HAVING COUNT(*) &gt; 3</code>.</p>\n'
                                     '<p>«Клиенты с выручкой больше 500» — это <code>HAVING SUM(amount) &gt; 500</code>. А «доставленные заказы» — всё ещё <code>WHERE status = '
                                     "'delivered'</code>. Во многих вопросах нужны оба.</p>\n"
                                     '<p class="pg"><b>PostgreSQL:</b> в <code>HAVING</code> нельзя использовать имя столбца из <code>AS</code>: пиши <code>HAVING SUM(amount) &gt; '
                                     '500</code>, а не <code>HAVING revenue &gt; 500</code>. (SQLite такое разрешает.) В <code>ORDER BY</code> имя работает в обоих.</p>\n'
                                     '<p><b>Пример:</b> категории, где не меньше 4 товаров.</p>'},
                     'example': 'SELECT category, COUNT(*) AS products\nFROM products\nGROUP BY category\nHAVING COUNT(*) >= 4;'},
                    {'id': 'an3.11',
                     'text': {'en': 'Which categories have an average price above 60? Category and average price (rounded to 2).',
                              'ru': 'В каких категориях средняя цена выше 60? Категория и средняя цена (округлённая до 2).'},
                     'answer': 'SELECT category, ROUND(AVG(price), 2) FROM products GROUP BY category HAVING AVG(price) > 60;'},
                    {'id': 'an3.12',
                     'text': {'en': 'Our VIP list: customers whose revenue from delivered orders is over 500. Customer id and revenue.',
                              'ru': 'Список VIP: клиенты, у которых выручка по доставленным заказам больше 500. Id клиента и выручка.'},
                     'answer': "SELECT customer_id, SUM(amount) FROM orders WHERE status = 'delivered' GROUP BY customer_id HAVING SUM(amount) > 500;"},
                    {'id': 'an3.13',
                     'text': {'en': 'Which customers have at least 2 <b>delivered</b> orders? Show only the customer id.',
                              'ru': 'У каких клиентов не меньше 2 <b>доставленных</b> заказов? Покажи только id клиента.'},
                     'answer': "SELECT customer_id FROM orders WHERE status = 'delivered' GROUP BY customer_id HAVING COUNT(*) >= 2;"},
                    {'id': 'an3.14',
                     'text': {'en': 'Monthly revenue: the month and the revenue of delivered orders, from January to December.',
                              'ru': 'Выручка по месяцам: месяц и выручка доставленных заказов, с января по декабрь.'},
                     'answer': "SELECT strftime('%Y-%m', order_date) AS month, SUM(amount) FROM orders WHERE status = 'delivered' GROUP BY month ORDER BY month;",
                     'section': {'en': 'D · Grouping by several columns and by months', 'ru': 'D · Группировка по нескольким столбцам и по месяцам'},
                     'intro': {'en': '<p>You can group by several columns: <code>GROUP BY status, promo_code</code> gives one row for every pair of values.</p>\n'
                                     "<p>You can also group by a calculation. The month of a date is <code>strftime('%Y-%m', order_date)</code> → <code>'2025-03'</code>.</p>\n"
                                     '<p class="pg"><b>PostgreSQL:</b> the month is <code>to_char(order_date, \'YYYY-MM\')</code> → <code>\'2025-03\'</code>, or '
                                     "<code>date_trunc('month', order_date)</code> → the date <code>2025-03-01</code>. <code>strftime</code> does not exist there.</p>\n"
                                     '<p><b>Example:</b> new customers per month of signup.</p>',
                               'ru': '<p>Группировать можно по нескольким столбцам: <code>GROUP BY status, promo_code</code> даёт строку на каждую пару значений.</p>\n'
                                     "<p>Можно группировать и по вычислению. Месяц даты — это <code>strftime('%Y-%m', order_date)</code> → <code>'2025-03'</code>.</p>\n"
                                     '<p class="pg"><b>PostgreSQL:</b> месяц — это <code>to_char(order_date, \'YYYY-MM\')</code> → <code>\'2025-03\'</code> или '
                                     "<code>date_trunc('month', order_date)</code> → дата <code>2025-03-01</code>. <code>strftime</code> там нет.</p>\n"
                                     '<p><b>Пример:</b> новые клиенты по месяцам регистрации.</p>'},
                     'example': "SELECT strftime('%Y-%m', signup_date) AS month, COUNT(*) AS new_customers\nFROM customers\nGROUP BY month\nORDER BY month;"},
                    {'id': 'an3.15',
                     'text': {'en': 'Which month had the <b>most delivered orders</b>? The month and the number of orders, one row.',
                              'ru': 'В каком месяце было <b>больше всего доставленных заказов</b>? Месяц и число заказов, одна строка.'},
                     'answer': "SELECT strftime('%Y-%m', order_date) AS month, COUNT(*) AS orders FROM orders WHERE status = 'delivered' GROUP BY month ORDER BY orders DESC LIMIT 1;"},
                    {'id': 'an3.16',
                     'text': {'en': 'Number of orders for every pair of status and promo code.', 'ru': 'Число заказов для каждой пары: статус и промокод.'},
                     'answer': 'SELECT status, promo_code, COUNT(*) FROM orders GROUP BY status, promo_code;'}]},
         {'id': 104,
          'track': 'analyst',
          'available': False,
          'title': {'en': 'JOIN: combining tables', 'ru': 'JOIN: соединяем таблицы'},
          'topics': {'en': 'INNER and LEFT JOIN, VLOOKUP, duplicated rows, customers without orders', 'ru': 'INNER и LEFT JOIN, ВПР, размножение строк, клиенты без заказов'}},
         {'id': 105,
          'track': 'analyst',
          'available': False,
          'title': {'en': 'CASE: segments', 'ru': 'CASE: сегменты'},
          'topics': {'en': 'Customer and order segments, conditional sums', 'ru': 'Сегменты клиентов и заказов, условные суммы'}},
         {'id': 106,
          'track': 'analyst',
          'available': False,
          'title': {'en': 'Dates and periods', 'ru': 'Даты и периоды'},
          'topics': {'en': 'Days, weeks, months, “last 30 days”, PostgreSQL equivalents', 'ru': 'Дни, недели, месяцы, «последние 30 дней», аналоги в PostgreSQL'}},
         {'id': 107,
          'track': 'analyst',
          'available': False,
          'title': {'en': 'CTE: queries step by step', 'ru': 'CTE: запросы по шагам'},
          'topics': {'en': 'WITH, subqueries, building a report in steps', 'ru': 'WITH, подзапросы, отчёт по шагам'}},
         {'id': 108,
          'track': 'analyst',
          'available': False,
          'title': {'en': 'Window functions', 'ru': 'Оконные функции'},
          'topics': {'en': 'ROW_NUMBER, RANK, LAG, running totals, month-over-month', 'ru': 'ROW_NUMBER, RANK, LAG, накопительные суммы, рост к прошлому месяцу'}},
         {'id': 109,
          'track': 'analyst',
          'available': False,
          'title': {'en': 'Business metrics', 'ru': 'Бизнес-метрики'},
          'topics': {'en': 'Average check, repeat purchases, retention, conversion', 'ru': 'Средний чек, повторные покупки, удержание, конверсия'}},
         {'id': 110,
          'track': 'analyst',
          'available': False,
          'title': {'en': "Final project: the shop's annual report", 'ru': 'Итоговый проект: годовой отчёт магазина'},
          'topics': {'en': 'Ten questions from the CEO, from data to conclusions', 'ru': 'Десять вопросов директора: от данных к выводам'}},

    ]
}
