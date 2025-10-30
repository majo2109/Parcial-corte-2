from fastapi import FastAPI
from database import create_db_and_tables

from routers import estudiantes, cursos, matriculas 

app = FastAPI(
    title="Sistema de Gestión de Universidad - Modular", 
    version="1.0.0",
    docs_url="/docs" 
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(estudiantes.router)
app.include_router(cursos.router)
app.include_router(matriculas.router)

@app.get("/")
def read_root():
    return {"message": "Sistema de Gestión de Universidad operativo. Ve a /docs para la documentación."}