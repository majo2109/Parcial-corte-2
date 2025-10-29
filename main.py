from fastapi import FastAPI
from db import create_tables
from routers import estudiantes, cursos, matriculas

def create_tables_lifespan():
    
    print("Iniciando aplicación: Creando base de datos y tablas...")
    create_tables() 
    
    yield 
    print("Apagando aplicación: Limpieza de recursos completada.")

app = FastAPI(
    lifespan=create_tables_lifespan, 
    title="Sistema de Gestión Universitaria"
)

app.include_router(estudiantes.router, tags=["Estudiantes"], prefix="/estudiantes")
app.include_router(cursos.router, tags=["Cursos"], prefix="/cursos")
app.include_router(matriculas.router, tags=["Matrículas"], prefix="/matriculas")

@app.get("/")
async def root():
    return {"message": "Bienvenido al Sistema de Gestión Universitaria"}

