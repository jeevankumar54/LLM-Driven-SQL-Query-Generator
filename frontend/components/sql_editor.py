import streamlit as st
from utils.state_management import update_generated_sql


def render_sql_editor(initial_sql: str = "", height: int = 200):
    sql_query = st.text_area(
        "SQL Query",
        value=initial_sql,
        height=height,
        key="sql_editor"
    )
    
    if sql_query != initial_sql:
        update_generated_sql(sql_query)
    
    return sql_query


def copy_to_clipboard_button(text: str, button_text: str = "Copy SQL", key: str = "copy_button"):
    if st.button(button_text, key=key):
        st.success("SQL copied to clipboard!")
        
        js_code = f"""
        <script>
        navigator.clipboard.writeText(`{text}`);
        </script>
        """
        st.components.v1.html(js_code, height=0)


def render_sql_with_explanation(sql: str, explanation: str = ""):
    st.subheader("Generated SQL")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        edited_sql = render_sql_editor(sql)
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        copy_to_clipboard_button(edited_sql)
    
    if explanation:
        with st.expander("SQL Explanation", expanded=False):
            st.markdown(explanation)
    
    return edited_sql