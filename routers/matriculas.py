from fastapi import APIRouter, HTTPException, status
from sqlmodel import select, and_, Session

from database import SessionDep
from models import Matricula, MatriculaBase, Estudiante, Curso

router = APIRouter(
    prefix="/matriculas",
    tags=["Matrículas"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def matricular_estudiante(
    *, 
    session: SessionDep, 
    matricula_in: MatriculaBase
):
    
    estudiante = session.get(Estudiante, matricula_in.estudiante_cedula)
    curso = session.get(Curso, matricula_in.curso_codigo)
    
    if not estudiante:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado.")
    if not curso:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso no encontrado.")
        
    statement_horario = select(Curso).join(Matricula).where(
        and_(
            Matricula.estudiante_cedula == matricula_in.estudiante_cedula,
            Curso.horario == curso.horario, 
            Curso.codigo != matricula_in.curso_codigo
        )
    )
    curso_conflicto = session.exec(statement_horario).first()

    if curso_conflicto:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail=f"Lógica de negocio: El estudiante ya está matriculado en el curso '{curso_conflicto.nombre}' con el mismo horario: {curso_conflicto.horario}."
        )

    existing_matricula = session.get(Matricula, (matricula_in.estudiante_cedula, matricula_in.curso_codigo))
    if existing_matricula:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El estudiante ya está matriculado en este curso.")

    matricula = Matricula.model_validate(matricula_in)
    session.add(matricula)
    session.commit()
    session.refresh(matricula)
    return {"message": "Estudiante matriculado exitosamente", "matricula": matricula}

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def desmatricular_estudiante(
    *, 
    session: SessionDep, 
    matricula_in: MatriculaBase
):
    matricula = session.get(Matricula, (matricula_in.estudiante_cedula, matricula_in.curso_codigo))
    
    if not matricula:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Matrícula no encontrada.")
        
    session.delete(matricula)
    session.commit()
    return {"ok": True}