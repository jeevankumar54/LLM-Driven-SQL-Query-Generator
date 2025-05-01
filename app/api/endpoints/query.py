from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.llm_service import LLMService
from app.services.database_service import DatabaseService
from app.api.dependencies import get_llm_service, get_database_service
from app.db.repository.query_history import (
    create_query_history,
    get_query_history,
    get_query_history_by_id,
    update_query_history_execution
)
from app.schemas.query import (
    QueryRequest,
    SQLQueryResult,
    QueryExecuteRequest,
    QueryExecuteResult,
    QueryHistoryCreate,
    QueryHistory
)


router = APIRouter()


@router.post("/generate", response_model=SQLQueryResult)
def generate_sql_query(
    query_request: QueryRequest,
    db: Session = Depends(get_db),
    llm_service: LLMService = Depends(get_llm_service)
):
    try:
        result = llm_service.generate_sql(
            db=db,
            natural_language_query=query_request.natural_language_query,
            schema_id=query_request.schema_id
        )
        
        query_history = QueryHistoryCreate(
            natural_language_query=query_request.natural_language_query,
            generated_sql=result.sql
        )
        create_query_history(db, query_history)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/execute", response_model=QueryExecuteResult)
def execute_sql_query(
    query_execute: QueryExecuteRequest,
    db: Session = Depends(get_db),
    db_service: DatabaseService = Depends(get_database_service)
):
    try:
        result = db_service.execute_query(
            db=db,
            sql_query=query_execute.sql,
            schema_id=query_execute.schema_id
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history", response_model=List[QueryHistory])
def get_queries_history(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    queries = get_query_history(db=db, skip=skip, limit=limit)
    return queries


@router.get("/history/{query_id}", response_model=QueryHistory)
def get_query_by_id(
    query_id: int,
    db: Session = Depends(get_db)
):
    query = get_query_history_by_id(db=db, query_id=query_id)
    if not query:
        raise HTTPException(status_code=404, detail=f"Query with id {query_id} not found")
    return query