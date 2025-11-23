from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from controllers.query_controller import process_question

st.title("AI SQL Query Generator (MVC)")

# Initialize session state
if "processing" not in st.session_state:
    st.session_state.processing = False

def start_processing():
    st.session_state.processing = True

with st.form("query_form"):
    question = st.text_input("Ask your question")
    
    submitted = st.form_submit_button(
        "Run Query",
        on_click=start_processing,
        disabled=st.session_state.processing
    )

if submitted and st.session_state.processing:
    with st.spinner("Processing your request..."):
        status, sql, rows, columns = process_question(question)

        # allow button again
        st.session_state.processing = False

        st.write("### Generated SQL:")
        st.code(sql)

        if status == "UNSAFE":
            st.error("Unsafe SQL detected. Query blocked.")
            st.stop()

        if status == "NO_SQL":
            st.warning("The AI could not generate a query for your request.")
            st.stop()

        if rows is None:
            st.success("Query executed successfully.")
        else:
            st.success("Data fetched successfully.")
            data = {columns[i]: [r[i] for r in rows] for i in range(len(columns))}
            st.dataframe(data)
