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
    """
    Crea un nuevo estudiante en la base de datos.

    Args:
        session: Dependencia de sesión de la base de datos.
        estudiante_in: Datos del nuevo estudiante (nombre, email, semestre, cédula).

    Raises:
        HTTPException 409: Si la cédula o el email ya existen.

    Returns:
        EstudianteRead: El objeto estudiante creado.
    """
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
    semestre: Optional[int] = Query(None)
):
    """
    Obtiene una lista de todos los estudiantes.

    Args:
        session: Dependencia de sesión de la base de datos.
        semestre: Parámetro opcional para filtrar estudiantes por semestre.

    Returns:
        List[EstudianteRead]: Lista de objetos estudiante.
    """
    statement = select(Estudiante)
    if semestre is not None:
        statement = statement.where(Estudiante.semestre == semestre)
        
    estudiantes = session.exec(statement).all()
    return estudiantes

@router.get("/{cedula}/", response_model=EstudianteReadWithCursos)
def read_estudiante(*, session: SessionDep, cedula: str):
    """
    Obtiene un estudiante por su cédula, incluyendo la lista de cursos matriculados.

    Args:
        session: Dependencia de sesión de la base de datos.
        cedula: Cédula del estudiante a buscar.

    Raises:
        HTTPException 404: Si el estudiante no es encontrado.

    Returns:
        EstudianteReadWithCursos: El objeto estudiante con sus cursos.
    """
    estudiante = session.get(Estudiante, cedula)
    if not estudiante:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado")
        
    cursos_matriculados = [matricula.curso for matricula in estudiante.matriculas]
    
    estudiante_read = EstudianteReadWithCursos.model_validate(estudiante)
    estudiante_read.cursos = [CursoRead.model_validate(curso) for curso in cursos_matriculados]
    return estudiante_read

@router.patch("/{cedula}/", response_model=EstudianteRead)
def update_estudiante(*, session: SessionDep, cedula: str, estudiante_in: EstudianteUpdate):
    """
    Actualiza parcialmente los datos de un estudiante por su cédula.

    Args:
        session: Dependencia de sesión de la base de datos.
        cedula: Cédula del estudiante a actualizar.
        estudiante_in: Datos a actualizar (nombre, email, semestre).

    Raises:
        HTTPException 404: Si el estudiante no es encontrado.
        HTTPException 409: Si el nuevo email ya está registrado.

    Returns:
        EstudianteRead: El objeto estudiante actualizado.
    """
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
    """
    Elimina un estudiante por su cédula.
    La matrícula asociada también será eliminada (comportamiento en cascada).

    Args:
        session: Dependencia de sesión de la base de datos.
        cedula: Cédula del estudiante a eliminar.

    Raises:
        HTTPException 404: Si el estudiante no es encontrado.
    """
    estudiante = session.get(Estudiante, cedula)
    if not estudiante:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado")

    session.delete(estudiante)
    session.commit()
    return {"ok": True}

@router.get("/{cedula}/cursos/", response_model=List[CursoRead])
def get_cursos_de_estudiante(*, session: SessionDep, cedula: str):
    """
    Obtiene la lista de cursos en los que un estudiante está matriculado.

    Args:
        session: Dependencia de sesión de la base de datos.
        cedula: Cédula del estudiante.

    Raises:
        HTTPException 404: Si el estudiante no es encontrado.

    Returns:
        List[CursoRead]: Lista de cursos.
    """
    estudiante = session.get(Estudiante, cedula)
    if not estudiante:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado")
        
    return [m.curso for m in estudiante.matriculas]