import os
from typing import Any, Generator, Annotated
from fastapi import Depends
from sqlmodel import create_engine, Session, SQLModel

from app.core.config import settings

environment = os.getenv("ENVIRONMENT")
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})

def create_db_and_tables():
    """
    Crea las tablas en la base de datos si no existen.
    """
    print("Making Test Tables...")
    SQLModel.metadata.create_all(engine)
    print("Test Tables Created.")

if environment == "DEV":
    print("Dev mode. Execute Test Tables Creation.")
    create_db_and_tables()
else:
    print(f"'{environment}' mode detected.")

try:
    with engine.connect() as connection:
        print("Successfully connected to Cloud SQL!")
except Exception as e:
    print(f"Error connecting to Cloud SQL: {e}")

def get_session() -> Generator[Session, Any, None]:
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
