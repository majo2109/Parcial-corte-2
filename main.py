from fastapi import FastAPI
from routers import estudiantes, cursos, matriculas
from db import create_db_and_tables


app = FastAPI(
    title="Sistema de Gestión Académica",
    description="API para gestionar estudiantes, cursos y matrículas con SQLModel",
    version="1.0.0"
)

create_db_and_tables()
app.include_router(estudiantes.router)
app.include_router(cursos.router)
app.include_router(matriculas.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API Académica"}

