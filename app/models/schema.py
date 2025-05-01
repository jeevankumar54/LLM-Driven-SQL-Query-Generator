from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class DatabaseSchema(Base):
    __tablename__ = "database_schemas"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=True)
    connection_string = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    tables = relationship("Table", back_populates="schema", cascade="all, delete-orphan")


class Table(Base):
    __tablename__ = "tables"
    
    id = Column(Integer, primary_key=True, index=True)
    schema_id = Column(Integer, ForeignKey("database_schemas.id"))
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    schema = relationship("DatabaseSchema", back_populates="tables")
    columns = relationship("Column", back_populates="table", cascade="all, delete-orphan")


class Column(Base):
    __tablename__ = "columns"
    
    id = Column(Integer, primary_key=True, index=True)
    table_id = Column(Integer, ForeignKey("tables.id"))
    name = Column(String, nullable=False)
    data_type = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    is_primary_key = Column(Boolean, default=False)
    is_foreign_key = Column(Boolean, default=False)
    references_table = Column(String, nullable=True)
    references_column = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    table = relationship("Table", back_populates="columns")