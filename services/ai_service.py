import google.generativeai as genai
import os
import streamlit as st

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]


genai.configure(api_key=GEMINI_API_KEY)

ALLOWED_TABLES = ["user_master", "designation_master"]

USER_TABLE_SCHEMA = """
TABLE: user_master
--------------------------------------------
Id (int, NOT NULL, Primary Key)
name (nvarchar(MAX), NULL)
pno_gatepass_no (nvarchar(MAX), NULL)
email (nvarchar(MAX), NULL)
mobile (nvarchar(MAX), NULL)
type (nvarchar(MAX), NULL)
designation_id (int, NULL)
dob (nvarchar(MAX), NULL)
doj (nvarchar(MAX), NULL)
ControllerId (int, NULL)
contractor_name (nvarchar(MAX), NULL)
created_by (int, NOT NULL)
created_datetime (datetime2, NOT NULL)
updated_by (int, NOT NULL)
updated_datetime (datetime2, NOT NULL)
status (nvarchar(MAX), NULL)
laststatus_by (int, NOT NULL)
laststatus_datetime (datetime2, NOT NULL)
ApproverId (int, NULL)
"""

DESIGNATION_TABLE_SCHEMA = """
TABLE: designation_master
--------------------------------------------
Id (int, NOT NULL, Primary Key)
designation_name (nvarchar(MAX), NULL)
created_by (int, NOT NULL)
created_datetime (datetime2, NOT NULL)
updated_by (int, NOT NULL)
updated_datetime (datetime2, NOT NULL)
status (nvarchar(MAX), NULL)
laststatus_by (int, NOT NULL)
laststatus_datetime (datetime2, NOT NULL)
"""


RELATIONSHIPS = """
RELATIONSHIPS:
user_master.designation_id = designation_master.Id
"""

def generate_sql(question):
    model = genai.GenerativeModel("gemini-2.5-pro")

    prompt = f"""
You are an SQL expert. Use only the tables listed below.

SCHEMA DETAILS:
{USER_TABLE_SCHEMA}

{DESIGNATION_TABLE_SCHEMA}

{RELATIONSHIPS}

RULES:
1. Only generate SQL Server (T-SQL).
2. Use JOIN only when needed based on relationships.
3. Never hallucinate columns.
4. Never select sensitive columns like: Id, password, created_by, updated_by, laststatus_by, created_datetime, updated_datetime, laststatus_datetime, ControllerId, ApproverId, designation_id.
5. Focus on user-facing data like: name, email, mobile, type, designation_name, status, dob, doj, contractor_name, pno_gatepass_no.
6. If question is unrelated to schema, reply:
   "I'm sorry, but I cannot help you with that."

User Question:
{question}

Return only the SQL query.
"""

    response = model.generate_content(prompt)
    sql = response.text.strip()
    
    # Remove markdown formatting
    sql = sql.replace("```sql", "").replace("```", "").strip()
    return sql
