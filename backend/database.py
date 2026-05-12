import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 🚀 ENTERPRISE FIX: Auto-fallback to secure local SQLite if no cloud DB is provided
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./inoptra_forgepro.db")

# SQLite needs special arguments to avoid multithreading issues in FastAPI
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()