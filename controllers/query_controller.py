from services.ai_service import generate_sql
from services.sql_safety import is_safe
from services.column_filter import filter_sensitive_columns
from models.db import execute_query

def process_question(question):
    """
    Processes a user question and returns status, SQL, rows, and columns.
    Returns tuple: (status, sql, rows, columns, error_message)
    """
    try:
        # Step 1: Ask Gemini to generate SQL
        try:
            sql = generate_sql(question)
        except Exception as e:
            return "AI_ERROR", "", None, None, f"AI generation failed: {str(e)}"

        # Check if AI refused to generate SQL
        if sql.startswith("I'm sorry") or "cannot help" in sql:
            return "NO_SQL", sql, None, None, None

        # Step 2: Validate SQL safety
        if not is_safe(sql):
            return "UNSAFE", sql, None, None, None

        # Step 3: Execute query
        try:
            rows, columns = execute_query(sql)
        except ConnectionError as e:
            return "DB_ERROR", sql, None, None, str(e)
        except Exception as e:
            return "QUERY_ERROR", sql, None, None, f"Query execution failed: {str(e)}"
        
        # Step 4: Filter sensitive columns
        if rows is not None and columns is not None:
            rows, columns = filter_sensitive_columns(rows, columns)
        
        return "OK", sql, rows, columns, None
    
    except Exception as e:
        return "ERROR", "", None, None, f"Unexpected error: {str(e)}"
