from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from db import get_session
from models import Estudiante, EstudianteCreate
import crud

router = APIRouter(prefix="/estudiantes", tags=["Estudiantes"])

@router.post("/", response_model=Estudiante)
def crear_estudiante(estudiante: EstudianteCreate, session: Session = Depends(get_session)):
    return crud.crear_estudiante(session, estudiante)

@router.get("/", response_model=list[Estudiante])
def listar_estudiantes(session: Session = Depends(get_session)):
    return crud.listar_estudiantes(session)

@router.get("/{estudiante_id}", response_model=Estudiante)
def obtener_estudiante(estudiante_id: int, session: Session = Depends(get_session)):
    estudiante = crud.obtener_estudiante(session, estudiante_id)
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return estudiante

@router.delete("/{estudiante_id}")
def eliminar_estudiante(estudiante_id: int, session: Session = Depends(get_session)):
    ok = crud.eliminar_estudiante(session, estudiante_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return {"ok": True}
