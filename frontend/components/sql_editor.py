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
    """
    Display a button that helps the user copy text to clipboard.
    Since direct clipboard access via JavaScript is not reliable in Streamlit,
    this function provides a workaround by showing the text in a
    temporary text area when the button is clicked.
    """
    if st.button(button_text, key=key):
        # Create a container for the copy functionality
        copy_container = st.container()
        
        with copy_container:
            st.success("SQL copied to selection area! Press Ctrl+A then Ctrl+C to copy.")
            # Display the text in a text area that makes it easy to select all and copy
            st.text_area(
                "Select all text (Ctrl+A) and copy (Ctrl+C):",
                value=text,
                height=100,
                key=f"copy_text_{key}"
            )
            # Add a button to hide the copy area after copying
            if st.button("Done", key=f"done_{key}"):
                # This doesn't actually hide the container, but on the next rerun it won't be shown
                st.session_state[f"hide_copy_{key}"] = True
                st.rerun()


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