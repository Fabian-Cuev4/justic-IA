# backend/app/core/session.py

import uuid
session_id = str(uuid.uuid4())

def get_session_id():
    return session_id
