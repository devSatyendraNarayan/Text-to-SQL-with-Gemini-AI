from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from controllers.query_controller import process_question

st.title("🤖 AI SQL Query Generator")

# Initialize session state
if "processing" not in st.session_state:
    st.session_state.processing = False
if "last_question" not in st.session_state:
    st.session_state.last_question = ""
if "last_error" not in st.session_state:
    st.session_state.last_error = None

def start_processing():
    st.session_state.processing = True

def retry_last_query():
    st.session_state.processing = True
    st.session_state.last_error = None

# Main query form
with st.form("query_form"):
    question = st.text_input("Ask your question", value=st.session_state.last_question)
    
    submitted = st.form_submit_button(
        "🚀 Run Query",
        on_click=start_processing,
        disabled=st.session_state.processing
    )

# Process the query
if submitted and st.session_state.processing:
    st.session_state.last_question = question
    
    with st.spinner("🔄 Processing your request..."):
        status, sql, rows, columns, error_msg = process_question(question)

        # Allow button again
        st.session_state.processing = False

        # Display generated SQL if available
        if sql:
            st.write("### 📝 Generated SQL:")
            st.code(sql, language="sql")

        # Handle different statuses
        if status == "UNSAFE":
            st.error("🚫 **Unsafe SQL detected.** Query blocked for security reasons.")
            st.stop()

        elif status == "NO_SQL":
            st.warning("⚠️ **The AI could not generate a query for your request.**")
            st.info("💡 Try rephrasing your question or asking about the available tables.")
            st.stop()

        elif status == "AI_ERROR":
            st.error(f"🤖 **AI Generation Error:**\n\n{error_msg}")
            st.session_state.last_error = error_msg
            if st.button("🔄 Try Again"):
                retry_last_query()
                st.rerun()
            st.stop()

        elif status == "DB_ERROR":
            st.error(f"🔌 **Database Connection Error:**\n\n{error_msg}")
            st.session_state.last_error = error_msg
            
            # Show helpful tips
            with st.expander("💡 Troubleshooting Tips"):
                st.markdown("""
                **Common solutions:**
                - Verify your database server is running
                - Check if the server address and port are correct
                - Ensure your firewall allows the connection
                - Confirm network connectivity
                - For Streamlit Cloud: Your database must be publicly accessible or use a VPN/tunnel
                """)
            
            if st.button("🔄 Try Again"):
                retry_last_query()
                st.rerun()
            st.stop()

        elif status == "QUERY_ERROR":
            st.error(f"⚠️ **Query Execution Error:**\n\n{error_msg}")
            st.session_state.last_error = error_msg
            if st.button("🔄 Try Again"):
                retry_last_query()
                st.rerun()
            st.stop()

        elif status == "ERROR":
            st.error(f"❌ **Unexpected Error:**\n\n{error_msg}")
            st.session_state.last_error = error_msg
            if st.button("🔄 Try Again"):
                retry_last_query()
                st.rerun()
            st.stop()

        elif status == "OK":
            # Success!
            if rows is None:
                st.success("✅ Query executed successfully.")
            else:
                st.success(f"✅ Data fetched successfully! ({len(rows)} rows)")
                data = {columns[i]: [r[i] for r in rows] for i in range(len(columns))}
                st.dataframe(data, use_container_width=True)
                
                # Download button
                import pandas as pd
                df = pd.DataFrame(data)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv,
                    file_name="query_results.csv",
                    mime="text/csv"
                )

