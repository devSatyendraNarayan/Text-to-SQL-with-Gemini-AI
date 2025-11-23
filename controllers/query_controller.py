from services.ai_service import generate_sql
from services.sql_safety import is_safe
from services.column_filter import filter_sensitive_columns
from models.db import execute_query

def process_question(question):
    # Step 1: Ask Gemini to generate SQL
    sql = generate_sql(question)

    # Check if AI refused to generate SQL
    if sql.startswith("I'm sorry") or "cannot help" in sql:
        return "NO_SQL", sql, None, None

    # Step 2: Validate SQL safety
    if not is_safe(sql):
        return "UNSAFE", sql, None, None

    # Step 3: Execute query
    rows, columns = execute_query(sql)
    
    # Step 4: Filter sensitive columns
    if rows is not None and columns is not None:
        rows, columns = filter_sensitive_columns(rows, columns)
    
    return "OK", sql, rows, columns
