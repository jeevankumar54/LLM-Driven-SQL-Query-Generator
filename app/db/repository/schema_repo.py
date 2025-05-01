from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.schema import DatabaseSchema, Table, Column
from app.schemas.schema import (
    DatabaseSchemaCreate,
    DatabaseSchema as DatabaseSchemaSchema,
    TableCreate,
    ColumnCreate
)


def create_database_schema(db: Session, schema: DatabaseSchemaCreate) -> DatabaseSchema:
    db_schema = DatabaseSchema(
        name=schema.name,
        description=schema.description,
        connection_string=schema.connection_string,
        is_active=schema.is_active
    )
    db.add(db_schema)
    db.commit()
    db.refresh(db_schema)
    
    for table_data in schema.tables:
        create_table(db, db_schema.id, table_data)
    
    return db_schema


def create_table(db: Session, schema_id: int, table: TableCreate) -> Table:
    db_table = Table(
        schema_id=schema_id,
        name=table.name,
        description=table.description
    )
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    
    for column_data in table.columns:
        create_column(db, db_table.id, column_data)
    
    return db_table


def create_column(db: Session, table_id: int, column: ColumnCreate) -> Column:
    db_column = Column(
        table_id=table_id,
        name=column.name,
        data_type=column.data_type,
        description=column.description,
        is_primary_key=column.is_primary_key,
        is_foreign_key=column.is_foreign_key,
        references_table=column.references_table,
        references_column=column.references_column
    )
    db.add(db_column)
    db.commit()
    db.refresh(db_column)
    return db_column


def get_all_database_schemas(db: Session, skip: int = 0, limit: int = 100) -> List[DatabaseSchema]:
    return db.query(DatabaseSchema).offset(skip).limit(limit).all()


def get_database_schema_by_id(db: Session, schema_id: int) -> Optional[DatabaseSchema]:
    return db.query(DatabaseSchema).filter(DatabaseSchema.id == schema_id).first()


def get_database_schema_by_name(db: Session, name: str) -> Optional[DatabaseSchema]:
    return db.query(DatabaseSchema).filter(DatabaseSchema.name == name).first()


def update_database_schema(
    db: Session, 
    schema_id: int, 
    schema_update: DatabaseSchemaCreate
) -> Optional[DatabaseSchema]:
    db_schema = get_database_schema_by_id(db, schema_id)
    if not db_schema:
        return None
    
    db_schema.name = schema_update.name
    db_schema.description = schema_update.description
    db_schema.connection_string = schema_update.connection_string
    db_schema.is_active = schema_update.is_active
    
    db.commit()
    db.refresh(db_schema)
    
    for table in db_schema.tables:
        db.delete(table)
    db.commit()
    
    for table_data in schema_update.tables:
        create_table(db, db_schema.id, table_data)
    
    return db_schema


def delete_database_schema(db: Session, schema_id: int) -> bool:
    db_schema = get_database_schema_by_id(db, schema_id)
    if not db_schema:
        return False
    
    db.delete(db_schema)
    db.commit()
    return True