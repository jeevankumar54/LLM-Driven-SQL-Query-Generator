import streamlit as st
import json
from utils.api_client import APIClient
from utils.state_management import (
    update_schema_list,
    update_selected_schema,
    display_error_if_any,
    set_error_message
)


def add_column_form():
    with st.form(key="add_column_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            column_name = st.text_input("Column Name", key="column_name")
            column_type = st.selectbox(
                "Data Type",
                ["INTEGER", "VARCHAR", "TEXT", "BOOLEAN", "DATE", "TIMESTAMP", "FLOAT", "DOUBLE", "DECIMAL"],
                key="column_type"
            )
            
        with col2:
            is_primary = st.checkbox("Primary Key", key="is_primary")
            is_foreign = st.checkbox("Foreign Key", key="is_foreign")
            
            if is_foreign:
                ref_table = st.text_input("Reference Table", key="ref_table")
                ref_column = st.text_input("Reference Column", key="ref_column")
            else:
                ref_table = ""
                ref_column = ""
        
        column_description = st.text_area("Column Description (Optional)", key="column_description")
        
        submitted = st.form_submit_button("Add Column")
        
        if submitted:
            return {
                "name": column_name,
                "data_type": column_type,
                "description": column_description,
                "is_primary_key": is_primary,
                "is_foreign_key": is_foreign,
                "references_table": ref_table if is_foreign else None,
                "references_column": ref_column if is_foreign else None
            }
    
    return None


def add_table_form():
    with st.form(key="add_table_form"):
        table_name = st.text_input("Table Name", key="table_name")
        table_description = st.text_area("Table Description (Optional)", key="table_description")
        
        submitted = st.form_submit_button("Create Table")
        
        if submitted:
            return {
                "name": table_name,
                "description": table_description,
                "columns": []
            }
    
    return None


def render_schema_manager(api_client: APIClient):
    st.title("Database Schema Manager")
    
    display_error_if_any()
    
    tab1, tab2, tab3 = st.tabs(["View Schemas", "Create Schema", "Import/Export"])
    
    with tab1:
        st.subheader("Available Database Schemas")
        
        # Get schemas
        schemas = api_client.get_schemas()
        update_schema_list(schemas)
        
        if not schemas:
            st.info("No database schemas available. Create one in the 'Create Schema' tab.")
        else:
            for schema in schemas:
                with st.expander(f"{schema['name']}", expanded=False):
                    st.markdown(f"**ID:** {schema['id']}")
                    
                    if schema.get("description"):
                        st.markdown(f"**Description:** {schema['description']}")
                    
                    st.markdown(f"**Connection String:** `{schema.get('connection_string', 'Not provided')}`")
                    
                    st.markdown("---")
                    st.markdown("### Tables")
                    
                    for table in schema.get("tables", []):
                        st.markdown(f"**{table['name']}**")
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
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"Edit Schema {schema['id']}", key=f"edit_{schema['id']}"):
                            # This would redirect to edit mode in a real app
                            st.session_state.editing_schema_id = schema['id']
                            st.rerun()
                    
                    with col2:
                        if st.button(f"Delete Schema {schema['id']}", key=f"delete_{schema['id']}"):
                            if api_client.delete_schema(schema['id']):
                                st.success(f"Schema {schema['name']} deleted successfully!")
                                st.rerun()
                            else:
                                set_error_message(f"Failed to delete schema {schema['name']}")
    
    with tab2:
        st.subheader("Create New Database Schema")
        
        with st.form(key="schema_form"):
            schema_name = st.text_input("Schema Name", key="schema_name")
            schema_description = st.text_area("Schema Description (Optional)", key="schema_description")
            connection_string = st.text_input(
                "Database Connection String",
                value="postgresql://username:password@localhost:5432/database",
                key="connection_string"
            )
            
            submitted = st.form_submit_button("Create Schema")
            
            if submitted:
                if not schema_name:
                    st.error("Schema name is required.")
                else:
                    # Create empty schema first
                    new_schema = {
                        "name": schema_name,
                        "description": schema_description,
                        "connection_string": connection_string,
                        "is_active": True,
                        "tables": []
                    }
                    
                    result = api_client.create_schema(new_schema)
                    
                    if result:
                        st.success(f"Schema '{schema_name}' created successfully! Now add tables and columns.")
                        update_selected_schema(result.get("id"))
                        st.rerun()
                    else:
                        set_error_message("Failed to create schema.")
        
        # If we're in table creation mode for a new schema
        if "editing_schema_id" in st.session_state:
            schema_id = st.session_state.editing_schema_id
            schema = api_client.get_schema_by_id(schema_id)
            
            if schema:
                st.subheader(f"Editing Schema: {schema['name']}")
                
                # Add table section
                st.markdown("### Add a New Table")
                new_table = add_table_form()
                
                if new_table:
                    # Get current schema
                    current_schema = api_client.get_schema_by_id(schema_id)
                    
                    if current_schema:
                        # Add new table to tables list
                        tables = current_schema.get("tables", [])
                        tables.append(new_table)
                        
                        # Update schema with new table
                        update_data = {
                            "name": current_schema["name"],
                            "description": current_schema.get("description", ""),
                            "connection_string": current_schema.get("connection_string", ""),
                            "is_active": current_schema.get("is_active", True),
                            "tables": tables
                        }
                        
                        result = api_client.update_schema(schema_id, update_data)
                        
                        if result:
                            st.success(f"Table '{new_table['name']}' added successfully!")
                            st.rerun()
                        else:
                            set_error_message("Failed to add table.")
                
                # Display existing tables and allow adding columns
                for i, table in enumerate(schema.get("tables", [])):
                    with st.expander(f"Table: {table['name']}", expanded=True):
                        st.markdown(f"**Name:** {table['name']}")
                        
                        if table.get("description"):
                            st.markdown(f"**Description:** {table['description']}")
                        
                        st.markdown("### Columns")
                        
                        # Display existing columns
                        for col in table.get("columns", []):
                            col_desc = f"- **{col['name']}** ({col['data_type']})"
                            if col.get("is_primary_key"):
                                col_desc += " PRIMARY KEY"
                            if col.get("is_foreign_key"):
                                col_desc += f" → {col.get('references_table')}.{col.get('references_column')}"
                            st.markdown(col_desc)
                        
                        st.markdown("### Add Column to This Table")
                        
                        new_column = add_column_form()
                        
                        if new_column:
                            # Get current schema
                            current_schema = api_client.get_schema_by_id(schema_id)
                            
                            if current_schema:
                                # Add new column to the table
                                tables = current_schema.get("tables", [])
                                if i < len(tables):
                                    if "columns" not in tables[i]:
                                        tables[i]["columns"] = []
                                    
                                    tables[i]["columns"].append(new_column)
                                    
                                    # Update schema with new column
                                    update_data = {
                                        "name": current_schema["name"],
                                        "description": current_schema.get("description", ""),
                                        "connection_string": current_schema.get("connection_string", ""),
                                        "is_active": current_schema.get("is_active", True),
                                        "tables": tables
                                    }
                                    
                                    result = api_client.update_schema(schema_id, update_data)
                                    
                                    if result:
                                        st.success(f"Column '{new_column['name']}' added successfully!")
                                        st.rerun()
                                    else:
                                        set_error_message("Failed to add column.")
                
                if st.button("Finish Editing Schema", type="primary"):
                    if "editing_schema_id" in st.session_state:
                        del st.session_state.editing_schema_id
                        st.rerun()
    
    with tab3:
        st.subheader("Import/Export Schema")
        
        # Export tab
        export_tab, import_tab = st.tabs(["Export Schema", "Import Schema"])
        
        with export_tab:
            schemas = api_client.get_schemas()
            
            if not schemas:
                st.info("No schemas available to export.")
            else:
                schema_options = [f"{schema['id']}: {schema['name']}" for schema in schemas]
                selected_schema_option = st.selectbox(
                    "Select Schema to Export",
                    options=schema_options,
                    key="export_schema_select"
                )
                
                if selected_schema_option:
                    schema_id = int(selected_schema_option.split(":")[0])
                    schema = api_client.get_schema_by_id(schema_id)
                    
                    if schema:
                        schema_json = json.dumps(schema, indent=2)
                        st.download_button(
                            label="Download Schema JSON",
                            data=schema_json,
                            file_name=f"{schema['name']}_schema.json",
                            mime="application/json"
                        )
                        
                        with st.expander("Preview JSON", expanded=False):
                            st.code(schema_json, language="json")
        
        with import_tab:
            st.markdown("Upload a schema JSON file to import it into the system.")
            
            uploaded_file = st.file_uploader("Choose a schema JSON file", type="json")
            
            if uploaded_file is not None:
                try:
                    schema_data = json.load(uploaded_file)
                    
                    # Remove ID fields to create a new schema
                    if "id" in schema_data:
                        del schema_data["id"]
                    
                    for table in schema_data.get("tables", []):
                        if "id" in table:
                            del table["id"]
                        if "schema_id" in table:
                            del table["schema_id"]
                        
                        for column in table.get("columns", []):
                            if "id" in column:
                                del column["id"]
                            if "table_id" in column:
                                del column["table_id"]
                    
                    # Validate required fields
                    if "name" not in schema_data:
                        st.error("Invalid schema: missing 'name' field.")
                    elif "tables" not in schema_data:
                        st.error("Invalid schema: missing 'tables' field.")
                    else:
                        # Add suffix to avoid duplicate names
                        schema_data["name"] = f"{schema_data['name']}_imported"
                        
                        if st.button("Import Schema", type="primary"):
                            result = api_client.create_schema(schema_data)
                            
                            if result:
                                st.success(f"Schema '{result['name']}' imported successfully!")
                                st.rerun()
                            else:
                                set_error_message("Failed to import schema.")
                
                except json.JSONDecodeError:
                    st.error("Invalid JSON file. Please upload a valid schema JSON.")
                except Exception as e:
                    st.error(f"Error processing the file: {e}")