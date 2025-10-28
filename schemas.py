from typing import Optional
from sqlmodel import SQLModel, Field

class EstudianteBase(SQLModel):
    nombre: str
    email: str
    semestre: int

class EstudianteCreate(EstudianteBase):
    pass


class EstudianteRead(EstudianteBase):
    id: int


class CursoBase(SQLModel):
    nombre: str
    codigo: str
    creditos: int


class CursoCreate(CursoBase):
    pass


class CursoRead(CursoBase):
    id: int


class MatriculaBase(SQLModel):
    estudiante_id: int
    curso_id: int


class MatriculaCreate(MatriculaBase):
    pass


class MatriculaRead(MatriculaBase):
    id: int

