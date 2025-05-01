# LLM-Driven SQL Query Generator

A full-stack application that uses LLM (Large Language Model) technology to generate SQL queries from natural language questions. This project features a FastAPI backend and a Streamlit frontend.

## Features

- **Natural Language to SQL**: Convert plain English questions to SQL queries
- **Database Schema Management**: Create, edit, and manage database schemas
- **Query Execution**: Execute generated SQL queries against connected databases
- **Query History**: Track and reuse previous queries
- **Import/Export**: Share database schemas between systems

## Architecture

The application follows a client-server architecture:

- **Backend**: FastAPI application with SQLAlchemy ORM
- **Frontend**: Streamlit web interface
- **Database**: PostgreSQL for application storage
- **LLM**: StarCoder model for SQL generation

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/sql-generator.git
   cd sql-generator
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. Initialize the database:
   ```bash
   alembic upgrade head
   ```

## Running the Application

1. Start the FastAPI backend:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

2. Start the Streamlit frontend (in a separate terminal):
   ```bash
   streamlit run frontend/app.py
   ```

3. Open your browser and navigate to:
   - Frontend: http://localhost:8501
   - Backend API docs: http://localhost:8000/docs

## Usage

### Adding a Database Schema

1. Navigate to the "Schema Manager" page
2. Click on "Create Schema" tab
3. Enter schema details and connection string
4. Add tables and columns to define your schema

### Generating SQL Queries

1. Navigate to the "Query Generator" page
2. Select a database schema (optional but recommended)
3. Enter your question in natural language
4. Click "Generate SQL" to create the query
5. Edit the generated SQL if needed
6. Click "Execute Query" to run the query

### Viewing Query History

1. Navigate to the "Query History" page
2. Browse through previous queries
3. Click on a query to view details
4. Reuse queries by clicking "Use This Query"

## Development

### Project Structure

```
sql-generator/
├── app/                         # FastAPI Backend
│   ├── api/                    # API endpoints
│   ├── core/                   # Core settings
│   ├── db/                     # Database session and models
│   ├── models/                 # SQLAlchemy models
│   ├── schemas/                # Pydantic schemas
│   └── services/               # Business logic
├── frontend/                    # Streamlit Frontend
│   ├── components/             # Reusable UI components
│   ├── pages/                  # Application pages
│   └── utils/                  # Frontend utilities
├── alembic/                     # Database migrations
├── tests/                       # Tests
└── .env                         # Environment variables
```

### Adding New Features

- **Backend**: Add new endpoints in `app/api/endpoints/`
- **Frontend**: Add new pages in `frontend/pages/`
- **Database**: Create migrations with `alembic revision -m "description"`

## License

[MIT License](LICENSE)

## Acknowledgements

- FastAPI: https://fastapi.tiangolo.com/
- Streamlit: https://streamlit.io/
- StarCoder: https://huggingface.co/bigcode/starcoder