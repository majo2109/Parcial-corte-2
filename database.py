from typing import Generator, Annotated
from sqlmodel import SQLModel, create_engine, Session
from fastapi import Depends

DATABASE_URL = "sqlite:///./universidad.db"
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

def create_db_and_tables():
    """
    Crea la base de datos y todas las tablas definidas en SQLModel.
    Esta función se ejecuta al iniciar la aplicación.
    """
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """
    Dependencia que genera y cierra una sesión de base de datos.
    Se utiliza para la inyección de dependencias en los endpoints de FastAPI.
    """
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]