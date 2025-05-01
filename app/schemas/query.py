from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel


class QueryRequest(BaseModel):
    natural_language_query: str
    schema_id: Optional[int] = None
    

class SQLQueryResult(BaseModel):
    sql: str
    explanation: Optional[str] = None


class QueryExecuteRequest(BaseModel):
    sql: str
    schema_id: int


class QueryExecuteResult(BaseModel):
    success: bool
    data: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None
    execution_time: Optional[int] = None
    result_count: Optional[int] = None


class QueryHistoryBase(BaseModel):
    natural_language_query: str
    generated_sql: str
    executed: bool = False
    execution_time: Optional[int] = None
    result_count: Optional[int] = None
    error: Optional[str] = None


class QueryHistoryCreate(QueryHistoryBase):
    pass


class QueryHistory(QueryHistoryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True