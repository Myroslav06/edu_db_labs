
DROP TABLE IF EXISTS Report;
DROP TABLE IF EXISTS quizResult;
DROP TABLE IF EXISTS Module_Quiz;
DROP TABLE IF EXISTS Module;
DROP TABLE IF EXISTS Course;
DROP TABLE IF EXISTS Answer;
DROP TABLE IF EXISTS Option;
DROP TABLE IF EXISTS Question;
DROP TABLE IF EXISTS QuizAssignment;
DROP TABLE IF EXISTS Quiz;
DROP TABLE IF EXISTS quizCategory;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Role;

CREATE TABLE Role (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE User (
    id INT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    last_name VARCHAR(100),
    first_name VARCHAR(100),
    role_id INT,
    FOREIGN KEY (role_id) REFERENCES Role(id)
);

CREATE TABLE quizCategory (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE Quiz (
    id INT PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    start_date DATE,
    end_date DATE,
    status VARCHAR(50),
    category_id INT,
    FOREIGN KEY (category_id) REFERENCES quizCategory(id)
);

CREATE TABLE QuizAssignment (
    id INT PRIMARY KEY,
    user_id INT,
    quiz_id INT,
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (quiz_id) REFERENCES Quiz(id)
);

CREATE TABLE Question (
    id INT PRIMARY KEY,
    quiz_id INT,
    text TEXT,
    question_type VARCHAR(50),
    FOREIGN KEY (quiz_id) REFERENCES Quiz(id)
);

CREATE TABLE Option (
    id INT PRIMARY KEY,
    question_id INT,
    text TEXT,
    FOREIGN KEY (question_id) REFERENCES Question(id)
);

CREATE TABLE Answer (
    id INT PRIMARY KEY,
    user_id INT,
    quiz_id INT,
    question_id INT,
    option_id INT,
    text_answer TEXT,
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (quiz_id) REFERENCES Quiz(id),
    FOREIGN KEY (question_id) REFERENCES Question(id),
    FOREIGN KEY (option_id) REFERENCES Option(id)
);

CREATE TABLE Course (
    id INT PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    duration_weeks INT
);

CREATE TABLE Module (
    id INT PRIMARY KEY,
    course_id INT,
    title VARCHAR(255),
    content TEXT,
    FOREIGN KEY (course_id) REFERENCES Course(id)
);

CREATE TABLE Module_Quiz (
    module_id INT,
    quiz_id INT,
    PRIMARY KEY (module_id, quiz_id),
    FOREIGN KEY (module_id) REFERENCES Module(id),
    FOREIGN KEY (quiz_id) REFERENCES Quiz(id)
);

CREATE TABLE quizResult (
    id INT PRIMARY KEY,
    quiz_id INT,
    respondent_count INT,
    FOREIGN KEY (quiz_id) REFERENCES Quiz(id)
);

CREATE TABLE Report (
    id INT PRIMARY KEY,
    quiz_result_id INT,
    user_id INT,
    format VARCHAR(50),
    content TEXT,
    created_at DATE,
    FOREIGN KEY (quiz_result_id) REFERENCES quizResult(id),
    FOREIGN KEY (user_id) REFERENCES User(id)
);

INSERT INTO Role (id, name) VALUES
(1, 'Адміністратор'),
(2, 'Експерт'),
(3, 'Користувач');

INSERT INTO User (id, email, last_name, first_name, role_id) VALUES
(1, 'admin@osvita.ua', 'Шевченко', 'Тарас', 1),
(2, 'expert@med.ua', 'Ковальчук', 'Олена', 2),
(3, 'student@edu.ua', 'Мельник', 'Андрій', 3);

INSERT INTO quizCategory (id, name) VALUES
(1, 'Освіта'),
(2, 'Охорона здоров’я'),
(3, 'Технології');

INSERT INTO Course (id, title, description, duration_weeks) VALUES
(1, 'Основи Python', 'Базовий курс з програмування мовою Python.', 6),
(2, 'Цифрова грамотність', 'Курс для підвищення цифрової компетентності.', 4);

INSERT INTO Module (id, course_id, title, content) VALUES
(1, 1, 'Змінні та типи даних', 'Теоретичні матеріали щодо типів змінних у Python.'),
(2, 1, 'Умовні оператори', 'Оператори if, elif, else.'),
(3, 2, 'Інтернет-безпека', 'Основи захисту персональних даних.'),
(4, 2, 'Електронні сервіси', 'Як користуватись державними онлайн-сервісами.');

INSERT INTO Quiz (id, title, description, start_date, end_date, status, category_id) VALUES
(1, 'Перевірка знань з Python', 'Опитування для перевірки базових знань з Python.', '2025-06-01', '2025-06-15', 'Заплановано', 3),
(2, 'Онлайн-безпека громадян', 'Оцінка обізнаності користувачів у сфері кібербезпеки.', '2025-06-10', '2025-06-20', 'Чернетка', 2);

INSERT INTO Module_Quiz (module_id, quiz_id) VALUES
(1, 1),
(3, 2);

INSERT INTO QuizAssignment (id, user_id, quiz_id) VALUES
(1, 2, 1),  -- Експерт
(2, 3, 2);  -- Користувач

INSERT INTO Question (id, quiz_id, text, question_type) VALUES
(1, 1, 'Що таке змінна у Python?', 'single_choice'),
(2, 1, 'Оберіть правильні типи даних у Python:', 'multiple_choice'),
(3, 2, 'Як захистити свій пароль онлайн?', 'text');

INSERT INTO Option (id, question_id, text) VALUES
(1, 1, 'Комірка для зберігання даних'),
(2, 1, 'Назва функції'),
(3, 2, 'int'),
(4, 2, 'str'),
(5, 2, 'html');

INSERT INTO Answer (id, user_id, quiz_id, question_id, option_id, text_answer) VALUES
(1, 2, 1, 1, 1, NULL),
(2, 2, 1, 2, 3, NULL),
(3, 2, 1, 2, 4, NULL),
(4, 3, 2, 3, NULL, 'Використовувати складні паролі та двофакторну автентифікацію');

INSERT INTO quizResult (id, quiz_id, respondent_count) VALUES
(1, 1, 1),
(2, 2, 1);

INSERT INTO Report (id, quiz_result_id, user_id, format, content, created_at) VALUES
(1, 1, 1, 'PDF', 'Звіт про проходження опитування з Python.', '2025-06-16'),
(2, 2, 1, 'DOCX', 'Звіт з опитування щодо безпеки в інтернеті.', '2025-06-21');
