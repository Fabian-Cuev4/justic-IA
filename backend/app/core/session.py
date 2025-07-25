#PATH: backend/app/core/session.py

import uuid

# Genera un identificador único de sesión cuando se carga el módulo. (usado para diferenciar casos)
session_id = str(uuid.uuid4())

# Función para obtener el identificador de sesión actual.
def get_session_id():
    return session_id
