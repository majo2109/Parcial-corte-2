from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select, Session
from typing import List, Optional

from database import SessionDep
from models import (
    Estudiante, EstudianteCreate, EstudianteUpdate, EstudianteRead, EstudianteReadWithCursos,
    CursoRead
)

router = APIRouter(
    prefix="/estudiantes",
    tags=["Estudiantes"]
)

@router.post("/", response_model=EstudianteRead, status_code=status.HTTP_201_CREATED)
def create_estudiante(*, session: SessionDep, estudiante_in: EstudianteCreate):
    existing_estudiante = session.get(Estudiante, estudiante_in.cedula)
    if existing_estudiante:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe un estudiante con esa cédula.")

    estudiante = Estudiante.model_validate(estudiante_in)
    session.add(estudiante)
    
    try:
        session.commit()
        session.refresh(estudiante)
        return estudiante
    except Exception as e:
        if "unique constraint" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El email ya está registrado.")
        raise

@router.get("/", response_model=List[EstudianteRead])
def read_estudiantes(
    *, 
    session: SessionDep, 
    semestre: Optional[int] = Query(None),
    offset: int = 0, 
    limit: int = Query(default=100, le=100)
):
    statement = select(Estudiante).offset(offset).limit(limit)
    if semestre is not None:
        statement = statement.where(Estudiante.semestre == semestre)
        
    estudiantes = session.exec(statement).all()
    return estudiantes

@router.get("/{cedula}/", response_model=EstudianteReadWithCursos)
def read_estudiante(*, session: SessionDep, cedula: str):
    estudiante = session.get(Estudiante, cedula)
    if not estudiante:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado")
        
    cursos_matriculados = [matricula.curso for matricula in estudiante.matriculas]
    
    estudiante_read = EstudianteReadWithCursos.model_validate(estudiante)
    estudiante_read.cursos = [CursoRead.model_validate(curso) for curso in cursos_matriculados]
    return estudiante_read

@router.patch("/{cedula}/", response_model=EstudianteRead)
def update_estudiante(*, session: SessionDep, cedula: str, estudiante_in: EstudianteUpdate):
    db_estudiante = session.get(Estudiante, cedula)
    if not db_estudiante:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado")

    update_data = estudiante_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_estudiante, key, value)
    
    session.add(db_estudiante)
    try:
        session.commit()
        session.refresh(db_estudiante)
        return db_estudiante
    except Exception as e:
        if "unique constraint" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El nuevo email ya está registrado.")
        raise

@router.delete("/{cedula}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_estudiante(*, session: SessionDep, cedula: str):
    estudiante = session.get(Estudiante, cedula)
    if not estudiante:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado")

    session.delete(estudiante)
    session.commit()
    return {"ok": True}

@router.get("/{cedula}/cursos/", response_model=List[CursoRead])
def get_cursos_de_estudiante(*, session: SessionDep, cedula: str):
    estudiante = session.get(Estudiante, cedula)
    if not estudiante:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado")
        
    return [m.curso for m in estudiante.matriculas]