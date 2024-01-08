import sqlite3

# Подключение к базе данных SQLite
conn = sqlite3.connect('patients.db')
c = conn.cursor()

# Обновление существующей таблицы patients, добавление новых столбцов для диагноза и лекарств
c.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        birth_date TEXT NOT NULL,
        complaints TEXT,
        ticket_number INTEGER,
        diagnosis TEXT,
        medication TEXT
    )
''')

# Создание таблиц для диагнозов и лекарств
c.execute('''
    CREATE TABLE IF NOT EXISTS diagnoses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        diagnosis TEXT,
        diagnosis_date DATE,
        FOREIGN KEY(patient_id) REFERENCES patients(id)
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS medications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        medication_name TEXT,
        dosage TEXT,
        start_date DATE,
        end_date DATE,
        FOREIGN KEY(patient_id) REFERENCES patients(id)
    )
''')


# Добавление двух пациентов в таблицу
patients = [
    ('Иван Иванов', '1980-04-12'),
    ('Мария Петрова', '1992-11-08'),
    ('Николай Сёмин', '2003-12-09')
]

c.executemany('INSERT INTO patients (full_name, birth_date) VALUES (?, ?)', patients)

# Проверка, что данные добавлены
c.execute('SELECT * FROM patients')
print(c.fetchall())
# Применение изменений в базе данных
conn.commit()

# Закрытие соединения с базой данных
conn.close()
