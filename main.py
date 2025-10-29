from fastapi import FastAPI
from db import init_db
from routers import estudiantes, cursos, matriculas

app = FastAPI(title="Proyecto FastAPI + SQLModel")

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(estudiantes.router)
app.include_router(cursos.router)
app.include_router(matriculas.router)

@app.get("/")
def root():
    return {"mensaje": "Bienvenido al sistema de gestión de cursos y estudiantes"}
