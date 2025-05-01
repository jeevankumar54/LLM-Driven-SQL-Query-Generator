import os
from typing import Any, Dict, Optional

from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "SQL Query Generator"
    
    DATABASE_URL: PostgresDsn
    
    LLM_API_KEY: Optional[str] = None
    LLM_MODEL: str = "bigcode/starcoder"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()