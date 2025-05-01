from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.declarative import declarative_base

from app.api.endpoints import query, schema
from app.core.config import settings


app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query.router, prefix=f"{settings.API_V1_STR}/query", tags=["query"])
app.include_router(schema.router, prefix=f"{settings.API_V1_STR}/schema", tags=["schema"])


@app.get("/")
def read_root():
    return {"message": "Welcome to SQL Query Generator API"}