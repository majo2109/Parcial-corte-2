from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from db import get_session
from models import Matricula, MatriculaCreate
import crud

router = APIRouter(prefix="/matriculas", tags=["Matriculas"])

@router.post("/", response_model=Matricula)
def crear_matricula(matricula: MatriculaCreate, session: Session = Depends(get_session)):
    return crud.crear_matricula(session, matricula)

@router.get("/", response_model=list[Matricula])
def listar_matriculas(session: Session = Depends(get_session)):
    return crud.listar_matriculas(session)

@router.get("/{matricula_id}", response_model=Matricula)
def obtener_matricula(matricula_id: int, session: Session = Depends(get_session)):
    matricula = crud.obtener_matricula(session, matricula_id)
    if not matricula:
        raise HTTPException(status_code=404, detail="Matricula no encontrada")
    return matricula

@router.delete("/{matricula_id}")
def eliminar_matricula(matricula_id: int, session: Session = Depends(get_session)):
    ok = crud.eliminar_matricula(session, matricula_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Matricula no encontrada")
    return {"ok": True}
