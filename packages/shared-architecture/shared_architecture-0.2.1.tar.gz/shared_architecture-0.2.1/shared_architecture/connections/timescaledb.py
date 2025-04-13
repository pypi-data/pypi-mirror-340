import os
import psycopg2
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

class TimescaleDBPool:
    def __init__(self, database_url: str):
        self.engine = create_engine(
            database_url,
            pool_size=10,
            max_overflow=5,
            pool_timeout=30,
            pool_recycle=1800
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self):
        return self.SessionLocal()

class TimescaleDBConnection:
    def __init__(self, database_url):
        self.engine = create_engine(
            database_url,
            pool_size=10,
            max_overflow=5,
            pool_timeout=30,
            pool_recycle=1800
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self):
        return self.SessionLocal()

    def connect(self):
        """
        Establish a connection to TimescaleDB using private sensitive keys.
        Returns:
            psycopg2.connection: Database connection object.
        """
        return psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),  # Use the environment variable directly
            dbname=os.getenv("POSTGRES_DATABASE")
        )