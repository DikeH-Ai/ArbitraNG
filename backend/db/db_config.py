# Imports
# Core SQLModel tools for ORM and DB engine
from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy import event

# Database Engine Configuration

# SQLite database file name
sqlite_file_name = "database.db"

# Full SQLite connection URL (used by SQLAlchemy)
sqlite_url = f"sqlite:///{sqlite_file_name}"

# Connection arguments: Needed for SQLite multithreaded access
connect_args = {"check_same_thread": False}

# Create the SQLAlchemy engine
engine = create_engine(
    sqlite_url,
    connect_args=connect_args,
    echo=True  # Echo SQL queries to console for debugging (turn off in prod)
)

# Enable FK enforcement on each new SQLite connection


@event.listens_for(engine, "connect")
def _enable_sqlite_fks(dbapi_con, con_record):
    # dbapi_con is a raw sqlite3.Connection
    cursor = dbapi_con.cursor()
    cursor.execute("PRAGMA foreign_keys=ON;")
    cursor.close()

# Database Initialization Function


def create_database_and_tables():
    """
    Creates all tables defined by SQLModel models.
    Called at application startup during development.
    """
    SQLModel.metadata.create_all(engine)


# Session Generator (Dependency)


def get_session():
    """
    FastAPI dependency function.
    Opens a new database session and ensures it is closed after use.
    Yields a session to be injected into route functions.
    """
    session = Session(engine)
    try:
        yield session  # Provide session to route
    finally:
        session.close()  # Ensure session is closed after request
