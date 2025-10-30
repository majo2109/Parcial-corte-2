from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select, func, Session
from typing import List, Optional

from database import SessionDep
from models import Curso, CursoCreate, CursoUpdate, CursoRead, CursoReadWithEstudiantes, EstudianteRead

router = APIRouter(
    prefix="/cursos",
    tags=["Cursos"]
)

@router.post("/", response_model=CursoRead, status_code=status.HTTP_201_CREATED)
def create_curso(*, session: SessionDep, curso_in: CursoCreate):
    existing_curso = session.get(Curso, curso_in.codigo)
    if existing_curso:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe un curso con ese código.")

    curso = Curso.model_validate(curso_in)
    session.add(curso)
    session.commit()
    session.refresh(curso)
    return curso

@router.get("/", response_model=List[CursoRead])
def read_cursos(
    *, 
    session: SessionDep, 
    creditos: Optional[int] = Query(None), 
    codigo: Optional[str] = Query(None), 
    offset: int = 0, 
    limit: int = Query(default=100, le=100)
):
    statement = select(Curso)
    if creditos is not None:
        statement = statement.where(Curso.creditos == creditos)
    if codigo is not None:
        statement = statement.where(func.lower(Curso.codigo) == func.lower(codigo))
        
    cursos = session.exec(statement.offset(offset).limit(limit)).all()
    return cursos

@router.get("/{codigo}/", response_model=CursoReadWithEstudiantes)
def read_curso(*, session: SessionDep, codigo: str):
    curso = session.get(Curso, codigo)
    if not curso:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso no encontrado")
        
    estudiantes_matriculados = [matricula.estudiante for matricula in curso.matriculas]
    
    curso_read = CursoReadWithEstudiantes.model_validate(curso)
    curso_read.estudiantes = [EstudianteRead.model_validate(estudiante) for estudiante in estudiantes_matriculados]
    return curso_read

@router.patch("/{codigo}/", response_model=CursoRead)
def update_curso(*, session: SessionDep, codigo: str, curso_in: CursoUpdate):
    db_curso = session.get(Curso, codigo)
    if not db_curso:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso no encontrado")

    update_data = curso_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_curso, key, value)
    
    session.add(db_curso)
    try:
        session.commit()
        session.refresh(db_curso)
        return db_curso
    except Exception as e:
        if "unique constraint" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Error de unicidad al actualizar.")
        raise

@router.delete("/{codigo}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_curso(*, session: SessionDep, codigo: str):
    curso = session.get(Curso, codigo)
    if not curso:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso no encontrado")

    session.delete(curso)
    session.commit()
    return {"ok": True}

@router.get("/{codigo}/estudiantes/", response_model=List[EstudianteRead])
def get_estudiantes_de_curso(*, session: SessionDep, codigo: str):
    curso = session.get(Curso, codigo)
    if not curso:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso no encontrado")
        
    return [m.estudiante for m in curso.matriculas]