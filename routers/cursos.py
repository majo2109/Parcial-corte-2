from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from db  import get_session
from models import Curso, CursoCreate
import crud

router = APIRouter(prefix="/cursos", tags=["Cursos"])

@router.post("/", response_model=Curso)
def crear_curso(curso: CursoCreate, session: Session = Depends(get_session)):
    return crud.crear_curso(session, curso)

@router.get("/", response_model=list[Curso])
def listar_cursos(session: Session = Depends(get_session)):
    return crud.listar_cursos(session)

@router.get("/{curso_id}", response_model=Curso)
def obtener_curso(curso_id: int, session: Session = Depends(get_session)):
    curso = crud.obtener_curso(session, curso_id)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso

@router.delete("/{curso_id}")
def eliminar_curso(curso_id: int, session: Session = Depends(get_session)):
    ok = crud.eliminar_curso(session, curso_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return {"ok": True}
