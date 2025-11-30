# NexusHub Backend

Production-ready FastAPI backend with Domain-Driven Design architecture.

## Project Structure

```
backend/
├── core/               # Shared kernel
├── domains/           # Business domains
├── infrastructure/    # External integrations
├── alembic/          # Database migrations
└── tests/            # Test suite
```

## Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload --port 8000
```

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
