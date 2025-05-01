from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.repository.schema_repo import (
    create_database_schema,
    get_all_database_schemas,
    get_database_schema_by_id,
    update_database_schema,
    delete_database_schema
)
from app.schemas.schema import (
    DatabaseSchemaCreate,
    DatabaseSchema,
    DatabaseSchemaList
)


router = APIRouter()


@router.post("", response_model=DatabaseSchema)
def create_schema(
    schema: DatabaseSchemaCreate,
    db: Session = Depends(get_db)
):
    try:
        db_schema = create_database_schema(db=db, schema=schema)
        return db_schema
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=DatabaseSchemaList)
def get_schemas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    schemas = get_all_database_schemas(db=db, skip=skip, limit=limit)
    return {"schemas": schemas}


@router.get("/{schema_id}", response_model=DatabaseSchema)
def get_schema(
    schema_id: int,
    db: Session = Depends(get_db)
):
    db_schema = get_database_schema_by_id(db=db, schema_id=schema_id)
    if not db_schema:
        raise HTTPException(status_code=404, detail=f"Schema with id {schema_id} not found")
    return db_schema


@router.put("/{schema_id}", response_model=DatabaseSchema)
def update_schema(
    schema_id: int,
    schema: DatabaseSchemaCreate,
    db: Session = Depends(get_db)
):
    db_schema = update_database_schema(db=db, schema_id=schema_id, schema_update=schema)
    if not db_schema:
        raise HTTPException(status_code=404, detail=f"Schema with id {schema_id} not found")
    return db_schema


@router.delete("/{schema_id}", response_model=bool)
def delete_schema(
    schema_id: int,
    db: Session = Depends(get_db)
):
    success = delete_database_schema(db=db, schema_id=schema_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Schema with id {schema_id} not found")
    return success