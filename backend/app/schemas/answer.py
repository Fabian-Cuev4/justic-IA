#PATH: backend/app/schemas/answer.py

from pydantic import BaseModel                      # Base para crear modelos de validación de datos en FastAPI
from typing import List

# Modelo de respuesta estándar del sistema JusticIA
class AnswerResponse(BaseModel):
    answer: str             # Respuesta generada por el modelo de IA
    sources: List[str]      # Lista de fuentes utilizadas (nombres de archivos, por ejemplo)
