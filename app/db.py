"""
This module handles database connections and session management
"""

from typing import Annotated

from sqlmodel import Session, create_engine, SQLModel
from fastapi import Depends, FastAPI


SQLITE_FILE_NAME = "db.sqlite3"
SQLITE_URL = f"sqlite:///{SQLITE_FILE_NAME}"

engine = create_engine(SQLITE_URL)

# crear tablas con sqlite
def create_all_tables(app:FastAPI):
    """
    Create all tables in the database
    
    Args:
        app: The FastAPI application
    
    Yields:
        None
    """
    SQLModel.metadata.create_all(engine)
    yield


def get_session():
    """
    Get a database session
     """
    with Session(engine) as session:
        # Se usa yield para que la sesión sea cerrada automáticamente cuando termine
        # Yield delega el control a la función que lo llama
        yield session

#Registra la sesión como una dependencia para todos los endpoints
SessionDep = Annotated[Session, Depends(get_session)]
