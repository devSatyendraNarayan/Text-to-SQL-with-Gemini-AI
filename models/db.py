import pyodbc
import os
from dotenv import load_dotenv
load_dotenv()

def get_connection():
    server = os.getenv("SQL_SERVER")
    database = os.getenv("SQL_DATABASE")
    user = os.getenv("SQL_USERNAME")
    password = os.getenv("SQL_PASSWORD")
    driver = "{ODBC Driver 17 for SQL Server}"

    if user and password:
        conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={user};PWD={password}"
    else:
        conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;"

    return pyodbc.connect(conn_str)


def execute_query(query):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query)

        if query.strip().lower().startswith("select"):
            rows = cursor.fetchall()
            columns = [c[0] for c in cursor.description]
            return rows, columns
        else:
            conn.commit()
            return None, None

    finally:
        conn.close()
