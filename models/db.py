import pyodbc
import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

# Try to get credentials from Streamlit secrets first (for cloud deployment)
# Fall back to environment variables for local development
try:
    SQL_SERVER = st.secrets["SQL_SERVER"]
    SQL_DATABASE = st.secrets["SQL_DATABASE"]
    SQL_USERNAME = st.secrets.get("SQL_USERNAME", "")
    SQL_PASSWORD = st.secrets.get("SQL_PASSWORD", "")
except (KeyError, FileNotFoundError):
    SQL_SERVER = os.getenv("SQL_SERVER")
    SQL_DATABASE = os.getenv("SQL_DATABASE")
    SQL_USERNAME = os.getenv("SQL_USERNAME", "")
    SQL_PASSWORD = os.getenv("SQL_PASSWORD", "")


def get_connection():
    """
    Establishes a connection to the SQL Server database.
    Raises appropriate exceptions if connection fails.
    """
    server = SQL_SERVER
    database = SQL_DATABASE
    user = SQL_USERNAME
    password = SQL_PASSWORD
    driver = "{ODBC Driver 17 for SQL Server}"

    # Add connection timeout (30 seconds)
    if user and password:
        conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={user};PWD={password};Connection Timeout=30;"
    else:
        conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;Connection Timeout=30;"

    try:
        return pyodbc.connect(conn_str)
    except pyodbc.OperationalError as e:
        error_msg = str(e)
        if "Login timeout expired" in error_msg or "HYT00" in error_msg:
            raise ConnectionError(
                "Database connection timeout. Please check:\n"
                "1. SQL Server address is correct and accessible\n"
                "2. Firewall allows connections\n"
                "3. SQL Server is running\n"
                "4. Network connection is stable"
            )
        elif "Login failed" in error_msg:
            raise ConnectionError(
                "Database login failed. Please check:\n"
                "1. Username and password are correct\n"
                "2. User has access to the database"
            )
        else:
            raise ConnectionError(f"Database connection error: {error_msg}")
    except Exception as e:
        raise ConnectionError(f"Unexpected database error: {str(e)}")


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
