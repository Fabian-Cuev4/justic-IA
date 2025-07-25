#PATH: backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Permite que el frontend (Streamlit) acceda al backend desde otro dominio.
from app.routes import query, casos 

# Inicialización de la aplicación FastAPI
app = FastAPI(title="JusticIA - Sistema Legal del Ecuador")

# Configura CORS para que el frontend pueda hacer peticiones sin restricciones al backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Las rutas definidas en query.py y casos.py se agrupan bajo el prefijo "/api/v1"
app.include_router(query.router, prefix="/api/v1")
app.include_router(casos.router, prefix="/api/v1")

# Ruta base para prueba rápida
@app.get("/")
def read_root():
    return {"message": "JusticIA API operativa"}

 