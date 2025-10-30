from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from db import get_session
from models import Matricula, MatriculaCreate, MatriculaRead, CursoRead, EstudianteRead
import crud
from typing import List

router = APIRouter(prefix="/matriculas", tags=["Matriculas"])

@router.post("/", response_model=MatriculaRead, status_code=status.HTTP_201_CREATED) 
def crear_matricula(matricula: MatriculaCreate, session: Session = Depends(get_session)):
    nueva_matricula = crud.crear_matricula(session, matricula)
    
    
    if isinstance(nueva_matricula, dict) and "error" in nueva_matricula:
        #
        if "Conflicto de horario" in nueva_matricula["error"]:
             raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=nueva_matricula["error"])
        else: 
             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=nueva_matricula["error"])
             
    return nueva_matricula

@router.get("/", response_model=List[MatriculaRead])
def listar_matriculas(session: Session = Depends(get_session)):
    return crud.listar_matriculas(session)


@router.get("/estudiante/{estudiante_id}/cursos", response_model=List[CursoRead])
def cursos_de_un_estudiante(estudiante_id: int, session: Session = Depends(get_session)):
    cursos = crud.listar_cursos_de_estudiante(session, estudiante_id)
    if not cursos:
        
        estudiante = crud.obtener_estudiante(session, estudiante_id)
        if not estudiante:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return cursos


@router.get("/curso/{curso_id}/estudiantes", response_model=List[EstudianteRead])
def estudiantes_de_un_curso(curso_id: int, session: Session = Depends(get_session)):
    estudiantes = crud.listar_estudiantes_de_curso(session, curso_id)
    if not estudiantes:
        
        curso = crud.obtener_curso(session, curso_id)
        if not curso:
            raise HTTPException(status_code=404, detail="Curso no encontrado")
    return estudiantes

@router.get("/{matricula_id}", response_model=MatriculaRead)
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