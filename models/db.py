import pyodbc
import os
from dotenv import load_dotenv
load_dotenv()

SQL_SERVER = os.getenv("SQL_SERVER")
SQL_DATABASE = os.getenv("SQL_DATABASE")
SQL_USERNAME = os.getenv("SQL_USERNAME")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")


def get_connection():
    server = SQL_SERVER
    database = SQL_DATABASE
    user = SQL_USERNAME
    password = SQL_PASSWORD
    driver = "{ODBC Driver 17 for SQL Server}"  # Ensure this is correct for your environment

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
