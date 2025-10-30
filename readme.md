Este trabajo es creado por Maria Jose Rincón 
contacto: majorincon2109@gmail.com
Estudiante de ingenieria de sistemas de la universidad Catolica de Colombia 

🎓 Sistema de Gestión de Universidad (API RESTful)
Este proyecto implementa una API REST para la gestión de Estudiantes y Cursos con una relación de muchos a muchos (N:M) a través de la entidad Matrícula.
✨ Características Principales
Tecnología: Desarrollado con FastAPI (Python) y SQLModel para la capa de ORM.

Base de Datos: SQLite (universidad.db) para almacenamiento local y ligero.

CRUD Completo: Implementación de las operaciones Create, Read (Listar y por ID), Update (Patch) y Delete para Estudiantes y Cursos.

Consultas Relacionales: Permite obtener un estudiante con todos sus cursos matriculados y un curso con todos sus estudiantes matriculados.

Filtros Avanzados:

Listar estudiantes filtrando por semestre.

Listar cursos filtrando por créditos o código.

¡Claro! Un README.md bien estructurado es esencial para la rúbrica. Aquí tienes una plantilla descriptiva que cubre todos los requisitos del proyecto (CRUD, lógica de negocio y filtros) y te guía para cumplir los criterios de entrega:

🎓 Sistema de Gestión de Universidad (API RESTful)
Este proyecto implementa una API REST para la gestión de Estudiantes y Cursos con una relación de muchos a muchos (N:M) a través de la entidad Matrícula.

✨ Características Principales
Tecnología: Desarrollado con FastAPI (Python) y SQLModel para la capa de ORM.

Base de Datos: SQLite (universidad.db) para almacenamiento local y ligero.

CRUD Completo: Implementación de las operaciones Create, Read (Listar y por ID), Update (Patch) y Delete para Estudiantes y Cursos.

Consultas Relacionales: Permite obtener un estudiante con todos sus cursos matriculados y un curso con todos sus estudiantes matriculados.

Filtros Avanzados:

Listar estudiantes filtrando por semestre.

Listar cursos filtrando por créditos o código.

🔒 Lógica de Negocio Implementada
Se han aplicado las siguientes validaciones y reglas para garantizar la integridad de los datos:

Unicidad de Cédula/Código: No se permite crear dos estudiantes con la misma cédula o dos cursos con el mismo código (Manejo de error 409 Conflict).

Validación de Email: El campo email en el modelo Estudiante está validado con una expresión regular.

Restricción de Horario: Un estudiante no puede matricularse en dos cursos cuyo horario sea idéntico, para evitar conflictos de agenda (Manejo de error 409 Conflict).

Comportamiento en Cascada: Al eliminar un estudiante, todas sus matrículas asociadas se eliminan automáticamente de la base de datos.

🚀 Despliegue y Ejecución
Sigue estos pasos para levantar la aplicación en tu entorno local.

1. Prerrequisitos
Python 3.9+

Gestor de entornos virtuales recomendado (venv o conda).

2. Instalación de Dependencias
Crea y activa tu entorno virtual:
python -m venv venv
source venv/bin/activate  # En Linux/macOS
.\venv\Scripts\activate   # En Windows


Instala todas las dependencias listadas en el archivo requirements.txt:

pip install -r requirements.txt


Inicia la aplicación con Uvicorn:

uvicorn main:app --reload

Una vez que el servidor esté activo, la API estará disponible en http://127.0.0.1:8000.

¡Claro! Un README.md bien estructurado es esencial para la rúbrica. Aquí tienes una plantilla descriptiva que cubre todos los requisitos del proyecto (CRUD, lógica de negocio y filtros) y te guía para cumplir los criterios de entrega:

🎓 Sistema de Gestión de Universidad (API RESTful)
Este proyecto implementa una API REST para la gestión de Estudiantes y Cursos con una relación de muchos a muchos (N:M) a través de la entidad Matrícula.

✨ Características Principales
Tecnología: Desarrollado con FastAPI (Python) y SQLModel para la capa de ORM.

Base de Datos: SQLite (universidad.db) para almacenamiento local y ligero.

CRUD Completo: Implementación de las operaciones Create, Read (Listar y por ID), Update (Patch) y Delete para Estudiantes y Cursos.

Consultas Relacionales: Permite obtener un estudiante con todos sus cursos matriculados y un curso con todos sus estudiantes matriculados.

Filtros Avanzados:

Listar estudiantes filtrando por semestre.

Listar cursos filtrando por créditos o código.

🔒 Lógica de Negocio Implementada
Se han aplicado las siguientes validaciones y reglas para garantizar la integridad de los datos:

Unicidad de Cédula/Código: No se permite crear dos estudiantes con la misma cédula o dos cursos con el mismo código (Manejo de error 409 Conflict).

Validación de Email: El campo email en el modelo Estudiante está validado con una expresión regular.

Restricción de Horario: Un estudiante no puede matricularse en dos cursos cuyo horario sea idéntico, para evitar conflictos de agenda (Manejo de error 409 Conflict).

Comportamiento en Cascada: Al eliminar un estudiante, todas sus matrículas asociadas se eliminan automáticamente de la base de datos.

🚀 Despliegue y Ejecución
Sigue estos pasos para levantar la aplicación en tu entorno local.

1. Prerrequisitos
Python 3.9+

Gestor de entornos virtuales recomendado (venv o conda).

2. Instalación de Dependencias
Crea y activa tu entorno virtual:

Bash

python -m venv venv
source venv/bin/activate  # En Linux/macOS
.\venv\Scripts\activate   # En Windows
Instala todas las dependencias listadas en el archivo requirements.txt:

Bash

pip install -r requirements.txt
3. Ejecución de la API
Inicia la aplicación con Uvicorn:

Bash

uvicorn main:app --reload
Una vez que el servidor esté activo, la API estará disponible en http://127.0.0.1:8000.

📖 Documentación y Endpoints
Para ver la documentación interactiva de la API (Swagger UI), donde puedes probar todos los endpoints, abre la siguiente URL en tu navegador:

🔗 Documentación interactiva: http://127.0.0.1:8000/docs

Gracias por su atención a mi trabajo 😁