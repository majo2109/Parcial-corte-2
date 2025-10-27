from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Matricula(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    estudiante_id: int = Field(foreign_key="estudiante.id")
    curso_id: int = Field(foreign_key="curso.id")
    
    estudiante: "Estudiante" = Relationship(back_populates="matriculas")
    curso: "Curso" = Relationship(back_populates="matriculas")

class Estudiante(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    email: str
    semestre: int 
    cursos: List["Curso"] = Relationship(back_populates="estudiantes", link_model=Matricula)

class Curso(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    creditos: int
    horario: str
    estudiantes: List[Estudiante] = Relationship(back_populates="cursos", link_model=Matricula)
    