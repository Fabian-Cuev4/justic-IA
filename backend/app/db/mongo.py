#PATH: backend/app/db/mongo.py
from pymongo import MongoClient
from datetime import datetime
import os

# Obtener URI desde variables de entorno
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("No se encontró MONGO_URI en las variables de entorno")

# Conexión con MongoDB Atlas
client = MongoClient(MONGO_URI)
db = client["justicia"]                     # Nombre de la base de datos
collection = db["respuestas"]

# Función para guardar una respuesta en la colección "respuestas"
def guardar_respuesta(question: str, answer: str, sources: list[str], session_id: str, file_bytes: bytes = None):
    doc = {
        "session_id": session_id,
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "answer": answer,
        "sources": sources
    }

    if file_bytes:
        doc["evidence_file"] = file_bytes                           # Almacena el archivo como bytes

    collection.insert_one(doc)

# Nueva función: obtener casos según su estado ('pendiente', 'sentenciado', etc)
def obtener_casos_por_estado(estado: str):
    collection = db["casos"]
    resultados = collection.find({"estado": estado})
    
    casos = []
    for doc in resultados:
        casos.append({
            "id": str(doc["_id"]),
            "nombre": doc.get("nombre", ""),
            "tipoDelito": doc.get("tipoDelito", ""),
            "estado": doc.get("estado", ""),
            "fecha": doc.get("fecha", ""),
            "veredicto": doc.get("veredicto", None)
        })
    return casos

# Función para obtener todos los casos sin filtrar
def obtener_casos():
    collection = db["casos"]
    resultados = collection.find()
    casos = []
    for doc in resultados:
        casos.append({
            "id": str(doc["_id"]),
            "nombre": doc.get("nombre", ""),
            "tipoDelito": doc.get("tipoDelito", ""),
            "estado": doc.get("estado", ""),
            "fecha": doc.get("fecha", ""),
            "veredicto": doc.get("veredicto", None)
        })
    return casos

# Función para insertar un nuevo caso judicial
def insertar_caso(caso: dict):
    casos_collection = db["casos"]
    casos_collection.insert_one(caso)

