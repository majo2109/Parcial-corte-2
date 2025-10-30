from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session

from database import SessionDep
from models import Matricula, MatriculaBase

router = APIRouter(
    prefix="/matriculas",
    tags=["Matrículas"]
)

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def desmatricular_estudiante(
    *, 
    session: SessionDep, 
    matricula_in: MatriculaBase
):
    """
    Elimina una matrícula específica (desmatricula un estudiante de un curso).

    Args:
        session: Dependencia de sesión de la base de datos.
        matricula_in: Objeto MatriculaBase con la cédula del estudiante y el código del curso.

    Raises:
        HTTPException 404: Si la matrícula no es encontrada.
    """
    matricula = session.get(Matricula, (matricula_in.estudiante_cedula, matricula_in.curso_codigo))
    
    if not matricula:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Matrícula no encontrada.")
        
    session.delete(matricula)
    session.commit()
    return {"ok": True}