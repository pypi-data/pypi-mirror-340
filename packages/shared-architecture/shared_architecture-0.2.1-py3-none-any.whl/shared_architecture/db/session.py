"""
Database Session Module

This module provides utilities for managing database connections and sessions
using SQLAlchemy. It dynamically constructs the database URL from environment
variables to ensure compatibility across multiple environments.
"""

import os  # Standard library
from sqlalchemy.orm import sessionmaker  # Third-party library
from sqlalchemy import create_engine  # Third-party library


def get_database_url() -> str:
    """
    Dynamically constructs the database URL from environment variables.

    Returns:
        str: The database connection URL.
    Raises:
        RuntimeError: If required database credentials are missing.
    """
    try:
        db_user = os.getenv("POSTGRES_USER", "traduser")
        db_password = os.getenv("POSTGRES_PASSWORD", "tradpass")
        db_host = os.getenv("POSTGRES_HOST", "localhost")
        db_port = os.getenv("POSTGRES_PORT", "5432")
        db_name = os.getenv("POSTGRES_DATABASE", "timescaledb")

        return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    except Exception as e:
        raise RuntimeError(f"Failed to construct database URL: {e}") from e


DATABASE_URL = get_database_url()
engine = create_engine(DATABASE_URL,
    pool_size=10,       # Maximum connections in the pool
    max_overflow=5,     # Connections that can overflow beyond pool_size
    pool_timeout=30,    # Time to wait for connection before throwing an error
    pool_recycle=1800   # Recycle connections after 1800 seconds
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Provide a database session generator.

    Yields:
        SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        