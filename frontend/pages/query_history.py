import streamlit as st
import pandas as pd
from datetime import datetime
from utils.api_client import APIClient
from utils.state_management import (
    update_query_history_list,
    update_generated_sql,
    display_error_if_any,
    set_error_message
)
from components.sql_editor import render_sql_with_explanation


def format_timestamp(timestamp_str):
    try:
        timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
        return timestamp.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return timestamp_str


def render_query_history(api_client: APIClient):
    st.title("Query History")
    
    display_error_if_any()
    
    with st.spinner("Loading query history..."):
        queries = api_client.get_query_history()
        update_query_history_list(queries)
    
    if not queries:
        st.info("No query history available. Generate some SQL queries first!")
        return
    
    # Convert to dataframe for easier display
    query_data = []
    for query in queries:
        query_data.append({
            "ID": query.get("id", ""),
            "Natural Language Query": query.get("natural_language_query", ""),
            "SQL Query": query.get("generated_sql", ""),
            "Executed": "✅" if query.get("executed", False) else "❌",
            "Execution Time (ms)": query.get("execution_time", "-"),
            "Result Count": query.get("result_count", "-"),
            "Created At": format_timestamp(query.get("created_at", ""))
        })
    
    df = pd.DataFrame(query_data)
    
    # Search functionality
    search_term = st.text_input("Search Query History", placeholder="Search by keywords...")
    
    if search_term:
        # Filter dataframe by search term
        mask = df["Natural Language Query"].str.contains(search_term, case=False) | \
               df["SQL Query"].str.contains(search_term, case=False)
        filtered_df = df[mask]
    else:
        filtered_df = df
    
    # Display queries in a table
    st.dataframe(
        filtered_df,
        column_config={
            "ID": st.column_config.NumberColumn("ID", width="small"),
            "Natural Language Query": st.column_config.TextColumn("Natural Language Query", width="medium"),
            "SQL Query": st.column_config.TextColumn("SQL Query", width="medium"),
            "Executed": st.column_config.TextColumn("Executed", width="small"),
            "Execution Time (ms)": st.column_config.NumberColumn("Execution Time (ms)", width="small"),
            "Result Count": st.column_config.NumberColumn("Result Count", width="small"),
            "Created At": st.column_config.TextColumn("Created At", width="small")
        },
        use_container_width=True,
        hide_index=True
    )
    
    # View details of a specific query
    st.subheader("View Query Details")
    
    query_ids = [str(query["id"]) for query in queries]
    selected_id = st.selectbox("Select Query ID", options=query_ids)
    
    if selected_id:
        query_id = int(selected_id)
        selected_query = None
        
        for query in queries:
            if query.get("id") == query_id:
                selected_query = query
                break
        
        if selected_query:
            st.markdown("### Natural Language Query")
            st.markdown(f"_{selected_query.get('natural_language_query', '')}_")
            
            st.markdown("### Generated SQL")
            sql = selected_query.get("generated_sql", "")
            render_sql_with_explanation(sql)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Use This Query", key="use_query"):
                    update_generated_sql(sql)
                    st.session_state.rerun_query_generator = True
                    st.success("Query loaded into the Query Generator!")
                    st.markdown("Go to the Query Generator page to edit and execute this query.")
            
            if selected_query.get("executed", False):
                st.markdown("### Execution Details")
                
                st.markdown(f"""
                **Execution Time:** {selected_query.get('execution_time', '-')} ms  
                **Results Count:** {selected_query.get('result_count', '-')} rows
                """)
                
                if selected_query.get("error"):
                    st.error(f"Execution Error: {selected_query.get('error')}")