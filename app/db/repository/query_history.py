from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.query import QueryHistory
from app.schemas.query import QueryHistoryCreate, QueryHistory as QueryHistorySchema


def create_query_history(db: Session, query_history: QueryHistoryCreate) -> QueryHistory:
    db_query_history = QueryHistory(**query_history.dict())
    db.add(db_query_history)
    db.commit()
    db.refresh(db_query_history)
    return db_query_history


def get_query_history(db: Session, skip: int = 0, limit: int = 100) -> List[QueryHistory]:
    return db.query(QueryHistory).order_by(QueryHistory.created_at.desc()).offset(skip).limit(limit).all()


def get_query_history_by_id(db: Session, query_id: int) -> Optional[QueryHistory]:
    return db.query(QueryHistory).filter(QueryHistory.id == query_id).first()


def update_query_history_execution(
    db: Session, 
    query_id: int, 
    executed: bool = True,
    execution_time: Optional[int] = None,
    result_count: Optional[int] = None,
    error: Optional[str] = None
) -> Optional[QueryHistory]:
    db_query = get_query_history_by_id(db, query_id)
    if not db_query:
        return None
    
    db_query.executed = executed
    db_query.execution_time = execution_time
    db_query.result_count = result_count
    db_query.error = error
    
    db.commit()
    db.refresh(db_query)
    return db_query