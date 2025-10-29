from fastapi import FastAPI
from routers import estudiantes, cursos, matriculas
from db import create_db_and_tables

app = FastAPI(
    lifespan=create_db_and_tables,
    title="universidad majo",
    version="1.0.0"
)
app.include_router(estudiantes.router, tags=["estudiantes"], prefix="/estudiantes")
app.include_router(cursos.router, tags=["cursos"], prefix="/cursos")
app.include_router(matriculas.router, tags=["matriculas"], prefix="/matriculas")

@app.get("/")
async def root():
    return {"message": "Bienvenido al sistema académico"}

@app.get("/saludo/{nombre}")
async def saludo(nombre: str):
    return {"message": f"Hola {nombre}, bienvenido a la universidad"}
