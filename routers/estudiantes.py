from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from db import get_session
from models import Estudiante, EstudianteCreate, EstudianteUpdate, EstudianteRead, EstudianteReadWithCursos
import crud
from typing import Optional, List

router = APIRouter(prefix="/estudiantes", tags=["Estudiantes"])

@router.post("/", response_model=EstudianteRead, status_code=status.HTTP_201_CREATED) 
def crear_estudiante(estudiante: EstudianteCreate, session: Session = Depends(get_session)):
    nuevo_estudiante = crud.crear_estudiante(session, estudiante)
    
    if nuevo_estudiante is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Estudiante con esta cédula ya existe")
    return nuevo_estudiante

@router.get("/", response_model=List[EstudianteRead])
def listar_estudiantes(semestre: Optional[int] = None, session: Session = Depends(get_session)):
   
    return crud.listar_estudiantes(session, semestre=semestre)

@router.get("/{estudiante_id}/cursos", response_model=EstudianteReadWithCursos) 
def obtener_estudiante_con_cursos(estudiante_id: int, session: Session = Depends(get_session)):
    estudiante_data = crud.obtener_estudiante_con_cursos(session, estudiante_id)
    if not estudiante_data:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return estudiante_data

@router.get("/{estudiante_id}", response_model=EstudianteRead)
def obtener_estudiante(estudiante_id: int, session: Session = Depends(get_session)):
    estudiante = crud.obtener_estudiante(session, estudiante_id)
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return estudiante


@router.patch("/{estudiante_id}", response_model=EstudianteRead)
def actualizar_estudiante(estudiante_id: int, estudiante_data: EstudianteUpdate, session: Session = Depends(get_session)):
    estudiante = crud.actualizar_estudiante(session, estudiante_id, estudiante_data)
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return estudiante

@router.delete("/{estudiante_id}")
def eliminar_estudiante(estudiante_id: int, session: Session = Depends(get_session)):
    ok = crud.eliminar_estudiante(session, estudiante_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return {"ok": True}