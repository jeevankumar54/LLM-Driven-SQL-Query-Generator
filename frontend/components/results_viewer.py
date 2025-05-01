import streamlit as st
import pandas as pd
import json
from typing import Dict, List, Any, Optional
import time


def render_results_viewer(results: Optional[Dict[str, Any]]):
    if not results:
        return
    
    if not results.get("success", False):
        st.error(f"Query execution failed: {results.get('error', 'Unknown error')}")
        return
    
    data = results.get("data", [])
    execution_time = results.get("execution_time", 0)
    result_count = results.get("result_count", 0)
    
    st.subheader("Query Results")
    
    st.markdown(f"""
    **Execution Time:** {execution_time} ms  
    **Rows Returned:** {result_count}
    """)
    
    if not data:
        st.info("Query executed successfully, but no data was returned.")
        return
    
    df = pd.DataFrame(data)
    
    with st.expander("Results Table", expanded=True):
        st.dataframe(df, use_container_width=True)
    
    csv = df.to_csv(index=False).encode('utf-8')
    json_str = df.to_json(orient='records')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            "Download as CSV",
            csv,
            "query_results.csv",
            "text/csv",
            key=f"download_csv_{int(time.time())}"
        )
    
    with col2:
        st.download_button(
            "Download as JSON",
            json_str,
            "query_results.json",
            "application/json",
            key=f"download_json_{int(time.time())}"
        )