import eel
import sqlite3

# Подключение к базе данных SQLite
conn = sqlite3.connect('patients.db')
c = conn.cursor()

# Создание таблицы, если она еще не существует
c.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        birth_date TEXT NOT NULL,
        complaints TEXT,
        ticket_number INTEGER
    )
''')
conn.commit()

# Функция для добавления нового пациента
@eel.expose
def add_patient(full_name, birth_date):
    c.execute('INSERT INTO patients (full_name, birth_date) VALUES (?, ?)', (full_name, birth_date))
    conn.commit()
    return c.lastrowid

# Функция для обновления жалоб пациента и присвоения ему номера талона
@eel.expose
def update_complaints(policy_number, complaints_list):
    # Преобразуем список жалоб в строку, разделяя жалобы символом ';'
    complaints_str = ';'.join(complaints_list)
    
    # Преобразуем policy_number в число
    try:
        policy_number_int = int(policy_number)
    except ValueError:
        return "Неверный формат номера полиса"

    # Проверяем, существует ли пациент
    c.execute('SELECT * FROM patients WHERE id=?', (policy_number_int,))
    patient = c.fetchone()
    
    if patient:
        # Если пациент существует, обновляем его жалобы и присваиваем талон
        ticket_number = generate_ticket_number()
        c.execute('UPDATE patients SET complaints=?, ticket_number=? WHERE id=?', (complaints_str, ticket_number, policy_number_int))
        conn.commit()
        return "Жалобы обновлены, номер талона: {}".format(ticket_number)
    else:
        return "Пациент с таким номером полиса не найден"




def generate_ticket_number():
    c.execute('SELECT MAX(ticket_number) FROM patients')
    max_ticket = c.fetchone()[0]
    return max_ticket + 1 if max_ticket else 1

# Функция для поиска пациента по номеру полиса или фамилии
@eel.expose
def search_patient(search_query):
    try:
        search_query_int = int(search_query)
    except ValueError:
        search_query_int = -1 

    c.execute("SELECT * FROM patients WHERE full_name LIKE ? OR ticket_number = ?", ('%'+search_query+'%', search_query_int))
    patient = c.fetchone()
    if patient:
        # Логируем для отладки
        print("Найден пациент:", patient)
        formatted_complaints = patient[3].split(';') if patient[3] else []
        return {
            'full_name': patient[1],
            'birth_date': patient[2],
            'complaints': formatted_complaints,
            'ticket_number': patient[4]
        }
    else:
        print("Пациент не найден")
        return "Не найдено"


@eel.expose
def add_diagnosis(patient_id, diagnosis, diagnosis_date):
    c.execute('INSERT INTO diagnoses (patient_id, diagnosis, diagnosis_date) VALUES (?, ?, ?)', (patient_id, diagnosis, diagnosis_date))
    conn.commit()

@eel.expose
def add_medication(patient_id, medication_name, dosage, start_date, end_date):
    c.execute('INSERT INTO medications (patient_id, medication_name, dosage, start_date, end_date) VALUES (?, ?, ?, ?, ?)', (patient_id, medication_name, dosage, start_date, end_date))
    conn.commit()


try:
    eel.init('web')
    eel.start('main.html', size=(1600, 1000))
except Exception as e:
    print("Произошла ошибка:", e)


@eel.expose
def add_patient(full_name, birth_date):
    c.execute('INSERT INTO patients (full_name, birth_date) VALUES (?, ?)', (full_name, birth_date))
    conn.commit()
    return c.lastrowid