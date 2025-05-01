from typing import Dict, List, Any, Optional, Tuple
import time
import sqlalchemy
from sqlalchemy import create_engine, text

from app.db.repository.schema_repo import get_database_schema_by_id
from app.schemas.query import QueryExecuteResult
from sqlalchemy.orm import Session


class DatabaseService:
    def __init__(self):
        self.engines = {}
    
    def _get_engine(self, connection_string: str):
        if connection_string not in self.engines:
            self.engines[connection_string] = create_engine(connection_string)
        return self.engines[connection_string]
    
    def execute_query(
        self,
        db: Session,
        sql_query: str,
        schema_id: int
    ) -> QueryExecuteResult:
        db_schema = get_database_schema_by_id(db, schema_id)
        if not db_schema:
            return QueryExecuteResult(
                success=False,
                error=f"Schema with id {schema_id} not found",
            )
        
        if not db_schema.connection_string:
            return QueryExecuteResult(
                success=False,
                error="No connection string provided for this schema",
            )
        
        try:
            engine = self._get_engine(db_schema.connection_string)
            
            start_time = time.time()
            
            with engine.connect() as connection:
                result = connection.execute(text(sql_query))
                rows = [dict(row._mapping) for row in result]
            
            execution_time = int((time.time() - start_time) * 1000)
            
            return QueryExecuteResult(
                success=True,
                data=rows,
                execution_time=execution_time,
                result_count=len(rows)
            )
            
        except Exception as e:
            return QueryExecuteResult(
                success=False,
                error=str(e),
            )