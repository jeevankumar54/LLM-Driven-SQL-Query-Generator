import streamlit as st
import time
from utils.api_client import APIClient
from utils.state_management import (
    update_generated_sql,
    update_query_results,
    update_schema_list,
    display_error_if_any,
    set_error_message
)
from components.sql_editor import render_sql_with_explanation
from components.results_viewer import render_results_viewer


def render_query_generator(api_client: APIClient):
    st.title("Natural Language to SQL")
    
    display_error_if_any()
    
    # Get schemas
    schemas = api_client.get_schemas()
    update_schema_list(schemas)
    
    # Schema selection
    schema_options = ["None"] + [f"{schema['id']}: {schema['name']}" for schema in schemas]
    selected_schema_option = st.selectbox(
        "Select Database Schema (Optional)",
        options=schema_options,
        key="schema_selectbox"
    )
    
    schema_id = None
    if selected_schema_option != "None":
        try:
            schema_id = int(selected_schema_option.split(":")[0])
        except:
            pass
    
    # If a schema is selected, show its details
    if schema_id:
        selected_schema = api_client.get_schema_by_id(schema_id)
        if selected_schema:
            with st.expander("Schema Details", expanded=False):
                for table in selected_schema.get("tables", []):
                    st.markdown(f"**Table: {table['name']}**")
                    if table.get("description"):
                        st.markdown(f"*{table['description']}*")
                    
                    columns_data = []
                    for column in table.get("columns", []):
                        column_str = f"- {column['name']} ({column['data_type']})"
                        if column.get("is_primary_key"):
                            column_str += " PRIMARY KEY"
                        if column.get("is_foreign_key"):
                            column_str += f" → {column.get('references_table')}.{column.get('references_column')}"
                        columns_data.append(column_str)
                    
                    for column_str in columns_data:
                        st.markdown(column_str)
                    
                    st.markdown("---")
    
    # Natural language query input
    st.subheader("Enter your question in natural language")
    nl_query = st.text_area(
        "For example: 'Show all customers from New York who made purchases over $1000 in the last month'",
        height=100,
        key="nl_query"
    )
    
    # Generate SQL button
    col1, col2 = st.columns([1, 4])
    with col1:
        generate_clicked = st.button("Generate SQL", type="primary", use_container_width=True)
    
    # Progress and generation
    if generate_clicked and nl_query:
        with st.spinner("Generating SQL query..."):
            response = api_client.generate_sql(natural_language_query=nl_query, schema_id=schema_id)
            
            if "error" in response and response["error"]:
                set_error_message(f"Failed to generate SQL: {response['error']}")
            else:
                sql = response.get("sql", "")
                explanation = response.get("explanation", "")
                update_generated_sql(sql, explanation)
    
    # Display generated SQL if available
    if st.session_state.generated_sql:
        sql = render_sql_with_explanation(
            st.session_state.generated_sql,
            st.session_state.sql_explanation
        )
        
        # Execute SQL button
        if schema_id:
            execute_clicked = st.button("Execute Query", type="primary", use_container_width=True)
            
            if execute_clicked:
                with st.spinner("Executing query..."):
                    results = api_client.execute_sql(sql_query=sql, schema_id=schema_id)
                    update_query_results(results)
        else:
            st.warning("To execute this query, please select a database schema above.")
        
        # Display query results if available
        if st.session_state.query_results:
            render_results_viewer(st.session_state.query_results)