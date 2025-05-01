from typing import Optional
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from app.core.config import settings
from app.schemas.query import SQLQueryResult
from app.db.repository.schema_repo import get_database_schema_by_id
from sqlalchemy.orm import Session


class LLMService:
    def __init__(self):
        self.model_name = settings.LLM_MODEL
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name, 
            torch_dtype=torch.float16,
            device_map="auto"
        )

    def _format_schema_for_prompt(self, db_schema):
        schema_str = f"Database Schema: {db_schema.name}\n\n"
        
        for table in db_schema.tables:
            schema_str += f"Table: {table.name}\n"
            if table.description:
                schema_str += f"Description: {table.description}\n"
            
            schema_str += "Columns:\n"
            for column in table.columns:
                schema_str += f"- {column.name} ({column.data_type})"
                if column.is_primary_key:
                    schema_str += " PRIMARY KEY"
                if column.is_foreign_key:
                    schema_str += f" REFERENCES {column.references_table}({column.references_column})"
                if column.description:
                    schema_str += f" - {column.description}"
                schema_str += "\n"
            
            schema_str += "\n"
        
        return schema_str

    def generate_sql(self, db: Session, natural_language_query: str, schema_id: Optional[int] = None) -> SQLQueryResult:
        schema_prompt = ""
        if schema_id:
            db_schema = get_database_schema_by_id(db, schema_id)
            if db_schema:
                schema_prompt = self._format_schema_for_prompt(db_schema)
        
        prompt = f"""
        {schema_prompt}
        
        Convert the following natural language query to SQL:
        
        {natural_language_query}
        
        SQL query:
        """
        
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=512,
                temperature=0.2,
                top_p=0.95,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        sql_part = response.split("SQL query:")[-1].strip()
        
        explanation = "Generated SQL based on the natural language query and provided schema."
        
        return SQLQueryResult(sql=sql_part, explanation=explanation)