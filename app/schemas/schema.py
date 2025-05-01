from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class ColumnBase(BaseModel):
    name: str
    data_type: str
    description: Optional[str] = None
    is_primary_key: bool = False
    is_foreign_key: bool = False
    references_table: Optional[str] = None
    references_column: Optional[str] = None


class ColumnCreate(ColumnBase):
    pass


class Column(ColumnBase):
    id: int
    table_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class TableBase(BaseModel):
    name: str
    description: Optional[str] = None


class TableCreate(TableBase):
    columns: List[ColumnCreate]


class Table(TableBase):
    id: int
    schema_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    columns: List[Column] = []

    class Config:
        orm_mode = True


class DatabaseSchemaBase(BaseModel):
    name: str
    description: Optional[str] = None
    connection_string: Optional[str] = None
    is_active: bool = True


class DatabaseSchemaCreate(DatabaseSchemaBase):
    tables: List[TableCreate]


class DatabaseSchema(DatabaseSchemaBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    tables: List[Table] = []

    class Config:
        orm_mode = True


class DatabaseSchemaList(BaseModel):
    schemas: List[DatabaseSchema]