"""
This module handles the pytest fixtures for the application
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session

from app.main import app
from app.db import get_session


SQLITE_FILE_NAME = "db.sqlite3"
SQLITE_URL = f"sqlite:///{SQLITE_FILE_NAME}"

# Configuración para crear la base de datos en memoria
# check_same_thread=False es para se este revisando si esta corriendo en el mismo thread
# con esto vamos a evitar que se ejecute un código en un thread y un código en otro thread
# poolclass se usa para evitar que se estén creando varias bases de datos
engine = create_engine(
    SQLITE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

@pytest.fixture(name='session')
def session_fixture():
    """
    Fixture for creating a session
    """
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    SQLModel.metadata.drop_all(engine) # limpiar memoria


# Se le esta diciendo que en un entorno de pruebas la sesión será sobre
# escrita para usar la declarada en el fixture
# Crear nueva sesión para no usar la misma que la de production
@pytest.fixture(name='client')
def client_fixture(session: Session):
    """
    Fixture for creating a client
    """
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)

    yield client

    app.dependency_overrides.clear()
