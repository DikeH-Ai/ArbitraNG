# Import
from fastapi import FastAPI
from contextlib import asynccontextmanager
from backend.db.db_config import create_database_and_tables
from backend.routes import router


# Application Lifespan & Database Initialization

@asynccontextmanager
async def lifespan(app: FastAPI):  # Development-only: remove or guard for production
    """
    Manage application startup and shutdown events.

    Startup:
    - Initialize or update database schema via SQLModel.

    Shutdown:
    - Perform any necessary cleanup (e.g., closing connections).
    """
    # Create database tables before handling any requests
    create_database_and_tables()
    print("✅ Database schema created on startup")
    yield
    # Placeholder for shutdown logic
    print("🛑 Application shutdown complete.")

# Instantiate FastAPI app with lifespan context
app = FastAPI(lifespan=lifespan)


# Router Registration

# Include main API router which aggregates product and listing routes
app.include_router(router)  # Main application routes


# Note:
# - For production, replace create_database_and_tables() with Alembic migrations.
