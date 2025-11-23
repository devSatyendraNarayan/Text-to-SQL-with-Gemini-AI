import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

# ----------------------------------------
# Base connection to master (for DB create)
# ----------------------------------------
def get_master_connection():
    server = os.getenv("SQL_SERVER")
    username = os.getenv("SQL_USERNAME")
    password = os.getenv("SQL_PASSWORD")

    driver = '{ODBC Driver 17 for SQL Server}'

    if username and password:
        conn_str = f"DRIVER={driver};SERVER={server};DATABASE=master;UID={username};PWD={password}"
    else:
        conn_str = f"DRIVER={driver};SERVER={server};DATABASE=master;Trusted_Connection=yes;"

    return pyodbc.connect(conn_str)


# ----------------------------------------
# Normal DB connection
# ----------------------------------------
def get_connection():
    server = os.getenv("SQL_SERVER")
    database = os.getenv("SQL_DATABASE")
    username = os.getenv("SQL_USERNAME")
    password = os.getenv("SQL_PASSWORD")

    driver = '{ODBC Driver 17 for SQL Server}'

    if username and password:
        conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
    else:
        conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;"

    return pyodbc.connect(conn_str)


# ----------------------------------------
# Create Database if not exists
# ----------------------------------------
def create_database():
    database = os.getenv("SQL_DATABASE")
    conn = get_master_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
    IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = '{database}')
    BEGIN
        CREATE DATABASE {database};
    END
    """)

    conn.commit()
    conn.close()


# ----------------------------------------
# Create Student Table if not exists
# ----------------------------------------
def create_student_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    IF NOT EXISTS (
        SELECT * FROM sysobjects WHERE name='student' AND xtype='U'
    )
    BEGIN
        CREATE TABLE student (
            id INT PRIMARY KEY,
            name VARCHAR(50),
            age INT,
            gender VARCHAR(10),
            course VARCHAR(50),
            fees INT
        );
    END
    """)

    conn.commit()
    conn.close()


# ----------------------------------------
# Insert initial data (if empty)
# ----------------------------------------
student_data = [
    (1, 'John Doe', 20, 'Male', 'Computer Science', 5000),
    (2, 'Jane Smith', 22, 'Female', 'Mathematics', 6000),
    (3, 'Bob Johnson', 21, 'Male', 'Physics', 5500),
    (4, 'Alice Brown', 23, 'Female', 'Chemistry', 6500),
    (5, 'David Davis', 24, 'Male', 'Biology', 7000),
]


def insert_student_data():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM student")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.executemany("""
            INSERT INTO student (id, name, age, gender, course, fees)
            VALUES (?, ?, ?, ?, ?, ?)
        """, student_data)
        conn.commit()

    conn.close()


# ----------------------------------------
# Execute SQL
# ----------------------------------------
def execute_query(query):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query)

        if query.strip().lower().startswith("select"):
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            return rows, columns
        else:
            conn.commit()
            return None, None

    except Exception as e:
        raise e

    finally:
        conn.close()


# Run all setup automatically
create_database()
create_student_table()
insert_student_data()
