import streamlit as st
from typing import Dict, List, Any, Optional


def initialize_session_state():
    if "generated_sql" not in st.session_state:
        st.session_state.generated_sql = ""
    
    if "sql_explanation" not in st.session_state:
        st.session_state.sql_explanation = ""
        
    if "query_results" not in st.session_state:
        st.session_state.query_results = None
        
    if "selected_schema_id" not in st.session_state:
        st.session_state.selected_schema_id = None
        
    if "schema_list" not in st.session_state:
        st.session_state.schema_list = []
        
    if "selected_query_id" not in st.session_state:
        st.session_state.selected_query_id = None
        
    if "query_history_list" not in st.session_state:
        st.session_state.query_history_list = []
        
    if "error_message" not in st.session_state:
        st.session_state.error_message = ""


def update_generated_sql(sql: str, explanation: Optional[str] = None):
    st.session_state.generated_sql = sql
    if explanation is not None:
        st.session_state.sql_explanation = explanation


def update_query_results(results: Dict[str, Any]):
    st.session_state.query_results = results


def update_selected_schema(schema_id: int):
    st.session_state.selected_schema_id = schema_id


def update_schema_list(schemas: List[Dict[str, Any]]):
    st.session_state.schema_list = schemas


def update_selected_query(query_id: int):
    st.session_state.selected_query_id = query_id


def update_query_history_list(queries: List[Dict[str, Any]]):
    st.session_state.query_history_list = queries


def set_error_message(message: str):
    st.session_state.error_message = message


def clear_error_message():
    st.session_state.error_message = ""


def display_error_if_any():
    if st.session_state.error_message:
        st.error(st.session_state.error_message)
        clear_error_message()