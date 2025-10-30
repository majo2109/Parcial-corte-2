from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from db  import get_session
from models import Curso, CursoCreate, CursoUpdate, CursoRead, CursoReadWithEstudiantes
import crud
from typing import Optional, List

router = APIRouter(prefix="/cursos", tags=["Cursos"])
@router.post("/", response_model=CursoRead, status_code=status.HTTP_201_CREATED) 
def crear_curso(curso: CursoCreate, session: Session = Depends(get_session)):
    nuevo_curso = crud.crear_curso(session, curso)
   
    if nuevo_curso is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Curso con este código ya existe")
    return nuevo_curso

@router.get("/", response_model=List[CursoRead])
def listar_cursos(creditos: Optional[int] = None, codigo: Optional[str] = None, session: Session = Depends(get_session)):
   
    return crud.listar_cursos(session, creditos=creditos, codigo=codigo)


@router.get("/{curso_id}/estudiantes", response_model=CursoReadWithEstudiantes)
def obtener_curso_con_estudiantes(curso_id: int, session: Session = Depends(get_session)):
    curso_data = crud.obtener_curso_con_estudiantes(session, curso_id)
    if not curso_data:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso_data

@router.get("/{curso_id}", response_model=CursoRead)
def obtener_curso(curso_id: int, session: Session = Depends(get_session)):
    curso = crud.obtener_curso(session, curso_id)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso

@router.patch("/{curso_id}", response_model=CursoRead)
def actualizar_curso(curso_id: int, curso_data: CursoUpdate, session: Session = Depends(get_session)):
    curso = crud.actualizar_curso(session, curso_id, curso_data)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso

@router.delete("/{curso_id}")
def eliminar_curso(curso_id: int, session: Session = Depends(get_session)):
    ok = crud.eliminar_curso(session, curso_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return {"ok": True}