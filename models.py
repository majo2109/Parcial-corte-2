from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class EstudianteBase(SQLModel):
    nombre: str
    codigo: str
    semestre: int

class CursoBase(SQLModel):
    nombre: str
    codigo: str
    creditos: int

class MatriculaBase(SQLModel):
    estudiante_id: int
    curso_id: int

class Estudiante(EstudianteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    matriculas: List["Matricula"] = Relationship(back_populates="estudiante")

class Curso(CursoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    matriculas: List["Matricula"] = Relationship(back_populates="curso")

class Matricula(MatriculaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    estudiante_id: int = Field(foreign_key="estudiante.id")
    curso_id: int = Field(foreign_key="curso.id")

    estudiante: Optional[Estudiante] = Relationship(back_populates="matriculas")
    curso: Optional[Curso] = Relationship(back_populates="matriculas")

class EstudianteCreate(EstudianteBase):
    pass

class EstudianteRead(EstudianteBase):
    id: int

class CursoCreate(CursoBase):
    pass

class CursoRead(CursoBase):
    id: int

class MatriculaCreate(MatriculaBase):
    pass

class MatriculaRead(MatriculaBase):
    id: int

    