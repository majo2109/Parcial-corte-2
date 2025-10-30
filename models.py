from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy.schema import PrimaryKeyConstraint

class MatriculaBase(SQLModel):
    estudiante_cedula: str = Field(foreign_key="estudiante.cedula", primary_key=True)
    curso_codigo: str = Field(foreign_key="curso.codigo", primary_key=True)

class Matricula(MatriculaBase, table=True):
    __tablename__ = "matricula"
    __table_args__ = (
        PrimaryKeyConstraint("estudiante_cedula", "curso_codigo"),
    )

    estudiante: "Estudiante" = Relationship(back_populates="matriculas")
    curso: "Curso" = Relationship(back_populates="matriculas")
    
class EstudianteBase(SQLModel):
    nombre: str = Field(index=True, min_length=2, max_length=100)
    email: str = Field(unique=True, index=True, regex=r"[^@]+@[^@]+\.[^@]+")
    semestre: int = Field(ge=1, le=12)

class CursoBase(SQLModel):
    nombre: str = Field(min_length=5, max_length=150)
    creditos: int = Field(ge=1, le=10)
    horario: str 

class Estudiante(EstudianteBase, table=True):
    cedula: str = Field(primary_key=True, index=True, unique=True, min_length=5, max_length=20)
    matriculas: List[Matricula] = Relationship(back_populates="estudiante", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

class EstudianteRead(EstudianteBase):
    cedula: str
    
class EstudianteReadWithCursos(EstudianteRead):
    cursos: List["CursoRead"] = [] 

class Curso(CursoBase, table=True):
    codigo: str = Field(primary_key=True, index=True, unique=True, min_length=3, max_length=10)
    matriculas: List[Matricula] = Relationship(back_populates="curso")
    
class CursoRead(CursoBase):
    codigo: str
    
class CursoReadWithEstudiantes(CursoRead):
    estudiantes: List[EstudianteRead] = []
    
class EstudianteCreate(EstudianteBase):
    cedula: str = Field(min_length=5, max_length=20)

class EstudianteUpdate(EstudianteBase):
    nombre: Optional[str] = None
    email: Optional[str] = None
    semestre: Optional[int] = None
    
class CursoCreate(CursoBase):
    codigo: str = Field(min_length=3, max_length=10)
    
class CursoUpdate(CursoBase):
    nombre: Optional[str] = None
    creditos: Optional[int] = None
    horario: Optional[str] = None
    
EstudianteReadWithCursos.model_rebuild()
CursoReadWithEstudiantes.model_rebuild()