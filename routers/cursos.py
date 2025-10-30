from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select, func, Session, and_
from typing import List, Optional

from database import SessionDep
from models import (
    Curso, CursoCreate, CursoUpdate, CursoRead, CursoReadWithEstudiantes, 
    EstudianteRead, MatriculaBase, Matricula, Estudiante
)

router = APIRouter(
    prefix="/cursos",
    tags=["Cursos"]
)

@router.post("/", response_model=CursoRead, status_code=status.HTTP_201_CREATED)
def create_curso(*, session: SessionDep, curso_in: CursoCreate):
    """
    Crea un nuevo curso en la base de datos.

    Args:
        session: Dependencia de sesión de la base de datos.
        curso_in: Datos del nuevo curso (nombre, créditos, horario, código).

    Raises:
        HTTPException 409: Si el código del curso ya existe.

    Returns:
        CursoRead: El objeto curso creado.
    """
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
    codigo: Optional[str] = Query(None) 
):
    """
    Obtiene una lista de todos los cursos, con soporte para filtros.

    Args:
        session: Dependencia de sesión de la base de datos.
        creditos: Parámetro opcional para filtrar cursos por cantidad de créditos.
        codigo: Parámetro opcional para filtrar cursos por código.

    Returns:
        List[CursoRead]: Lista de objetos curso.
    """
    statement = select(Curso)
    if creditos is not None:
        statement = statement.where(Curso.creditos == creditos)
    if codigo is not None:
        statement = statement.where(func.lower(Curso.codigo) == func.lower(codigo))
        
    cursos = session.exec(statement).all()
    return cursos

@router.get("/{codigo}/", response_model=CursoReadWithEstudiantes)
def read_curso(*, session: SessionDep, codigo: str):
    """
    Obtiene un curso por su código, incluyendo la lista de estudiantes matriculados.

    Args:
        session: Dependencia de sesión de la base de datos.
        codigo: Código del curso a buscar.

    Raises:
        HTTPException 404: Si el curso no es encontrado.

    Returns:
        CursoReadWithEstudiantes: El objeto curso con sus estudiantes.
    """
    curso = session.get(Curso, codigo)
    if not curso:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso no encontrado")
        
    estudiantes_matriculados = [matricula.estudiante for matricula in curso.matriculas]
    
    curso_read = CursoReadWithEstudiantes.model_validate(curso)
    curso_read.estudiantes = [EstudianteRead.model_validate(estudiante) for estudiante in estudiantes_matriculados]
    return curso_read

@router.patch("/{codigo}/", response_model=CursoRead)
def update_curso(*, session: SessionDep, codigo: str, curso_in: CursoUpdate):
    """
    Actualiza parcialmente los datos de un curso por su código.

    Args:
        session: Dependencia de sesión de la base de datos.
        codigo: Código del curso a actualizar.
        curso_in: Datos a actualizar (nombre, créditos, horario).

    Raises:
        HTTPException 404: Si el curso no es encontrado.
        HTTPException 409: Si hay conflicto de unicidad al actualizar.

    Returns:
        CursoRead: El objeto curso actualizado.
    """
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
    """
    Elimina un curso por su código.

    Args:
        session: Dependencia de sesión de la base de datos.
        codigo: Código del curso a eliminar.

    Raises:
        HTTPException 404: Si el curso no es encontrado.
    """
    curso = session.get(Curso, codigo)
    if not curso:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso no encontrado")

    session.delete(curso)
    session.commit()
    return {"ok": True}

@router.post("/{codigo}/estudiantes/", status_code=status.HTTP_201_CREATED)
def add_estudiante_to_curso(
    *, 
    session: SessionDep, 
    codigo: str, 
    matricula_data: MatriculaBase
):
    """
    Matricula un estudiante en el curso especificado.

    Args:
        session: Dependencia de sesión de la base de datos.
        codigo: Código del curso (de la URL).
        matricula_data: Datos de la matrícula (debe contener el estudiante_cedula y el curso_codigo).

    Raises:
        HTTPException 400: Si el código de la URL no coincide con el del cuerpo.
        HTTPException 404: Si el estudiante o el curso no son encontrados.
        HTTPException 409: Si el estudiante ya está matriculado en el curso, o si hay conflicto de horario (Lógica de Negocio).

    Returns:
        dict: Mensaje de éxito y el objeto matrícula.
    """
    if codigo != matricula_data.curso_codigo:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El código de curso en la URL y el cuerpo deben coincidir.")
        
    estudiante = session.get(Estudiante, matricula_data.estudiante_cedula)
    curso = session.get(Curso, codigo)
    
    if not estudiante:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado.")
    if not curso:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso no encontrado.")
        
    statement_horario = select(Curso).join(Matricula).where(
        and_(
            Matricula.estudiante_cedula == matricula_data.estudiante_cedula,
            Curso.horario == curso.horario, 
            Curso.codigo != codigo
        )
    )
    curso_conflicto = session.exec(statement_horario).first()

    if curso_conflicto:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail=f"Lógica de negocio: El estudiante ya está matriculado en el curso '{curso_conflicto.nombre}' con el mismo horario: {curso_conflicto.horario}."
        )

    existing_matricula = session.get(Matricula, (matricula_data.estudiante_cedula, codigo))
    if existing_matricula:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El estudiante ya está matriculado en este curso.")

    matricula = Matricula.model_validate(matricula_data)
    session.add(matricula)
    session.commit()
    session.refresh(matricula)
    return {"message": f"Estudiante {estudiante.cedula} matriculado exitosamente en el curso {curso.codigo}", "matricula": matricula}


@router.get("/{codigo}/estudiantes/", response_model=List[EstudianteRead])
def get_estudiantes_de_curso(*, session: SessionDep, codigo: str):
    """
    Obtiene la lista de estudiantes matriculados en un curso.

    Args:
        session: Dependencia de sesión de la base de datos.
        codigo: Código del curso.

    Raises:
        HTTPException 404: Si el curso no es encontrado.

    Returns:
        List[EstudianteRead]: Lista de estudiantes.
    """
    curso = session.get(Curso, codigo)
    if not curso:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso no encontrado")
        
    return [m.estudiante for m in curso.matriculas]