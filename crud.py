from sqlmodel import Session, select
from models import Estudiante, Curso, Matricula, EstudianteCreate, CursoCreate, MatriculaCreate

def crear_estudiante(session: Session, data: EstudianteCreate):
    estudiante = Estudiante.model_validate(data)
    session.add(estudiante)
    session.commit()
    session.refresh(estudiante)
    return estudiante

def listar_estudiantes(session: Session):
    return session.exec(select(Estudiante)).all()

def obtener_estudiante(session: Session, estudiante_id: int):
    return session.get(Estudiante, estudiante_id)

def eliminar_estudiante(session: Session, estudiante_id: int):
    estudiante = session.get(Estudiante, estudiante_id)
    if estudiante:
        session.delete(estudiante)
        session.commit()
        return True
    return False


def crear_curso(session: Session, data: CursoCreate):
    curso = Curso.model_validate(data)
    session.add(curso)
    session.commit()
    session.refresh(curso)
    return curso

def listar_cursos(session: Session):
    return session.exec(select(Curso)).all()

def obtener_curso(session: Session, curso_id: int):
    return session.get(Curso, curso_id)

def eliminar_curso(session: Session, curso_id: int):
    curso = session.get(Curso, curso_id)
    if curso:
        session.delete(curso)
        session.commit()
        return True
    return False

def crear_matricula(session: Session, data: MatriculaCreate):
    matricula = Matricula.model_validate(data)
    session.add(matricula)
    session.commit()
    session.refresh(matricula)
    return matricula

def listar_matriculas(session: Session):
    return session.exec(select(Matricula)).all()

def obtener_matricula(session: Session, matricula_id: int):
    return session.get(Matricula, matricula_id)

def eliminar_matricula(session: Session, matricula_id: int):
    matricula = session.get(Matricula, matricula_id)
    if matricula:
        session.delete(matricula)
        session.commit()
        return True
    return False
