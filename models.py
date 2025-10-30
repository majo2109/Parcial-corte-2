from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class EstudianteBase(SQLModel):
    nombre: str
    cedula: str = Field(index=True, unique=True) 
    email: Optional[str] = None 
    semestre: int
    
class CursoBase(SQLModel):
    nombre: str
    codigo: str = Field(index=True, unique=True) 
    creditos: int
    horario: str 

class MatriculaBase(SQLModel):
    estudiante_id: int
    curso_id: int

class Estudiante(EstudianteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    matriculas: List["Matricula"] = Relationship(
        back_populates="estudiante",
        sa_relationship_args={"cascade": "all, delete-orphan"}
    )

class Curso(CursoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    matriculas: List["Matricula"] = Relationship(
        back_populates="curso",
        sa_relationship_args={"cascade": "all, delete-orphan"}
    )

class Matricula(MatriculaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    estudiante_id: int = Field(foreign_key="estudiante.id")
    curso_id: int = Field(foreign_key="curso.id")

    estudiante: Optional[Estudiante] = Relationship(back_populates="matriculas")
    curso: Optional[Curso] = Relationship(back_populates="matriculas")

class EstudianteReadWithCursos(EstudianteBase):
    id: int
    cursos: List["CursoRead"] 
    

class CursoReadWithEstudiantes(CursoBase):
    id: int
    estudiantes: List["EstudianteRead"] 

class EstudianteCreate(EstudianteBase):
    pass

class EstudianteUpdate(SQLModel):
    nombre: Optional[str] = None
    email: Optional[str] = None
    semestre: Optional[int] = None
    
class EstudianteRead(EstudianteBase):
    id: int

class CursoCreate(CursoBase):
    pass

class CursoUpdate(SQLModel):
    nombre: Optional[str] = None
    creditos: Optional[int] = None
    horario: Optional[str] = None

class CursoRead(CursoBase):
    id: int

class MatriculaCreate(MatriculaBase):
    pass

class MatriculaRead(MatriculaBase):
    id: int

EstudianteReadWithCursos.model_rebuild()
CursoReadWithEstudiantes.model_rebuild()