"""
Database configuration and session management.
Uses SQLite for simple, file-based storage.
"""
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

logger = logging.getLogger(__name__)

# SQLite database file - created in project root
DATABASE_URL = "sqlite:///./addresses.db"

# Create engine with SQLite settings
# check_same_thread=False needed for FastAPI's async request handling
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False  # Set True to log SQL queries for debugging
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()


def get_db():
    """
    Dependency that provides a database session per request.
    Ensures proper cleanup after each request completes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all database tables on application startup."""
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
