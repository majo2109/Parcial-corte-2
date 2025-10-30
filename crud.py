from sqlmodel import Session, select
from models import Estudiante, Curso, Matricula, EstudianteCreate, CursoCreate, MatriculaCreate, EstudianteUpdate, CursoUpdate, CursoRead, EstudianteRead
from typing import Optional, List


def crear_estudiante(session: Session, data: EstudianteCreate):

    existing_estudiante = session.exec(select(Estudiante).where(Estudiante.cedula == data.cedula)).first()
    if existing_estudiante:
        
        return None 
        
    estudiante = Estudiante.model_validate(data)
    session.add(estudiante)
    session.commit()
    session.refresh(estudiante)
    return estudiante


def listar_estudiantes(session: Session, semestre: Optional[int] = None) -> List[Estudiante]:
   
    query = select(Estudiante)
    if semestre is not None:
        query = query.where(Estudiante.semestre == semestre)
    return session.exec(query).all()


def obtener_estudiante(session: Session, estudiante_id: int):
    return session.get(Estudiante, estudiante_id)


def obtener_estudiante_con_cursos(session: Session, estudiante_id: int):
  
    estudiante = session.get(Estudiante, estudiante_id)
    if not estudiante:
        return None
        
    cursos = [
        CursoRead.model_validate(matricula.curso)
        for matricula in estudiante.matriculas
        if matricula.curso
    ]
    
  
    return {
        "id": estudiante.id,
        "nombre": estudiante.nombre,
        "cedula": estudiante.cedula,
        "email": estudiante.email,
        "semestre": estudiante.semestre,
        "cursos": cursos
    }


def actualizar_estudiante(session: Session, estudiante_id: int, data: EstudianteUpdate):
    estudiante = session.get(Estudiante, estudiante_id)
    if not estudiante:
        return None
   
    for key, value in data.model_dump(exclude_unset=True).items(): 
        setattr(estudiante, key, value)
    session.add(estudiante)
    session.commit()
    session.refresh(estudiante)
    return estudiante


def eliminar_estudiante(session: Session, estudiante_id: int):
    
    estudiante = session.get(Estudiante, estudiante_id)
    if estudiante:
        session.delete(estudiante)
        session.commit()
        return True
    return False



def crear_curso(session: Session, data: CursoCreate):
   
    existing_curso = session.exec(select(Curso).where(Curso.codigo == data.codigo)).first()
    if existing_curso:
        
        return None 
        
    curso = Curso.model_validate(data)
    session.add(curso)
    session.commit()
    session.refresh(curso)
    return curso


def listar_cursos(session: Session, creditos: Optional[int] = None, codigo: Optional[str] = None) -> List[Curso]:
   
    query = select(Curso)
    if creditos is not None:
        query = query.where(Curso.creditos == creditos)
    if codigo is not None:
        query = query.where(Curso.codigo == codigo)
        
    return session.exec(query).all()


def obtener_curso(session: Session, curso_id: int):
    return session.get(Curso, curso_id)

def obtener_curso_con_estudiantes(session: Session, curso_id: int):
 
    curso = session.get(Curso, curso_id)
    if not curso:
        return None
        
    estudiantes = [
        EstudianteRead.model_validate(matricula.estudiante)
        for matricula in curso.matriculas
        if matricula.estudiante
    ]

    return {
        "id": curso.id,
        "nombre": curso.nombre,
        "codigo": curso.codigo,
        "creditos": curso.creditos,
        "horario": curso.horario,
        "estudiantes": estudiantes
    }


def actualizar_curso(session: Session, curso_id: int, data: CursoUpdate):
    curso = session.get(Curso, curso_id)
    if not curso:
        return None
    for key, value in data.model_dump(exclude_unset=True).items(): 
        setattr(curso, key, value)
    session.add(curso)
    session.commit()
    session.refresh(curso)
    return curso


def eliminar_curso(session: Session, curso_id: int):
   
    curso = session.get(Curso, curso_id)
    if curso:
        session.delete(curso)
        session.commit()
        return True
    return False


def crear_matricula(session: Session, data: MatriculaCreate):
 
    

    nuevo_curso = session.get(Curso, data.curso_id)
    if not nuevo_curso:
        return {"error": "Curso no existe"} 

    
    horario_conflicto = session.exec(
        select(Matricula)
        .join(Curso)
        .where(Matricula.estudiante_id == data.estudiante_id)
        .where(Curso.horario == nuevo_curso.horario)
    ).first()

    if horario_conflicto:
        return {"error": "Conflicto de horario: el estudiante ya tiene un curso a esa hora."} 
        
   
    matricula_existente = session.exec(
        select(Matricula)
        .where(Matricula.estudiante_id == data.estudiante_id)
        .where(Matricula.curso_id == data.curso_id)
    ).first()

    if matricula_existente:
        return {"error": "El estudiante ya está matriculado en este curso."}


  
    matricula = Matricula.model_validate(data)
    session.add(matricula)
    session.commit()
    session.refresh(matricula)
    return matricula


def listar_cursos_de_estudiante(session: Session, estudiante_id: int) -> List[CursoRead]:

    cursos = session.exec(
        select(Curso)
        .join(Matricula)
        .where(Matricula.estudiante_id == estudiante_id)
    ).all()
    return [CursoRead.model_validate(c) for c in cursos]


def listar_estudiantes_de_curso(session: Session, curso_id: int) -> List[EstudianteRead]:
   
    estudiantes = session.exec(
        select(Estudiante)
        .join(Matricula)
        .where(Matricula.curso_id == curso_id)
    ).all()
    return [EstudianteRead.model_validate(e) for e in estudiantes]


def listar_matriculas(session: Session):
    return session.exec(select(Matricula)).all()


def obtener_matricula(session: Session, matricula_id: int):
    return session.get(Matricula, matricula_id)


def actualizar_matricula(session: Session, matricula_id: int, data: MatriculaCreate):
    matricula = session.get(Matricula, matricula_id)
    if not matricula:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(matricula, key, value)
    session.add(matricula)
    session.commit()
    session.refresh(matricula)
    return matricula


def eliminar_matricula(session: Session, matricula_id: int):
    matricula = session.get(Matricula, matricula_id)
    if matricula:
        session.delete(matricula)
        session.commit()
        return True
    return False