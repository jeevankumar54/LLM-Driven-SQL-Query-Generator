import streamlit as st
import os

# from dotenv import load_dotenv
# load_dotenv()

# Hardcode the API_HOST value
API_HOST = "http://localhost:8000"

from utils.api_client import APIClient
from utils.state_management import initialize_session_state
from components.sql_editor import render_sql_editor
from pages.query_generator import render_query_generator
from pages.schema_manager import render_schema_manager
from pages.query_history import render_query_history

API_HOST = os.getenv("API_HOST", "http://localhost:8000")

st.set_page_config(
    page_title="SQL Query Generator",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    initialize_session_state()
    
    api_client = APIClient(base_url=API_HOST)
    
    st.sidebar.title("SQL Query Generator")
    
    page = st.sidebar.radio(
        "Navigate to:",
        ["Query Generator", "Schema Manager", "Query History"]
    )
    
    st.sidebar.divider()
    st.sidebar.info("This application uses LLM technology to generate SQL queries from natural language.")
    
    if page == "Query Generator":
        render_query_generator(api_client)
    elif page == "Schema Manager":
        render_schema_manager(api_client)
    elif page == "Query History":
        render_query_history(api_client)

if __name__ == "__main__":
    main()