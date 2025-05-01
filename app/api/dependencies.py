from typing import Generator
from fastapi import Depends

from app.db.session import get_db
from app.services.llm_service import LLMService
from app.services.database_service import DatabaseService


def get_llm_service() -> LLMService:
    return LLMService()


def get_database_service() -> DatabaseService:
    return DatabaseService()