#PATH: backend/app/routes/casos.py

from fastapi import APIRouter, Query, HTTPException, UploadFile, File, Form
from typing import List
from pydantic import BaseModel
from bson.binary import Binary
from bson import ObjectId
import json
from datetime import datetime
from app.db.mongo import obtener_casos_por_estado, insertar_caso
from app.loaders.pdf_loader import extract_text_from_pdf
from app.llm.rag_chain import build_qa_chain
from app.vectorstore.temp_vectorstore import TemporaryVectorStoreBuilder
from app.schemas.answer import AnswerResponse
from app.db.mongo import db
from collections import defaultdict

# Crear router para agrupar los endpoints relacionados a "casos".    
router = APIRouter()

# Modelo de respuesta
class Caso(BaseModel):
    id: str
    nombre: str
    estado: str
    tipoDelito: str
    fecha: str  # puedes usar datetime si lo prefieres
    veredicto: str | None = None
    
# ---

# Endpoint: OBTENER CASOS con un estado específico
@router.get("/casos", response_model=List[Caso])
async def listar_casos(estado: str = Query(..., description="Filtrar casos por estado")):
    try:
        casos = obtener_casos_por_estado(estado)  # Consulta MongoDB por estado
        return casos                              # Devuelve la lista como JSON
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los casos: {e}")

# ---    

# Endpoint: OBTENER TODOS LOS CASOS SIN FILTRO
@router.get("/casos/todos", response_model=List[Caso])
async def obtener_todos_casos():
    try:
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
                "veredicto": doc.get("veredicto")
            })
        return casos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener todos los casos: {e}")

# CREAR UN NUEVO CASO.
@router.post("/casos")
async def crear_caso(
    caso: str = Form(...),
    partePolicial: UploadFile = File(...)
):
    try:
        # Convertir el string JSON del campo 'caso' a diccionario
        caso_dict = json.loads(caso)

        # Leer contenido del archivo y convertir a binario
        contenido = await partePolicial.read()
        caso_dict["partePolicial"] = Binary(contenido)
        
        # Estado por defecto si no vino
        if "estado" not in caso_dict:
            caso_dict["estado"] = "pendiente"

        # Fecha por defecto si no vino
        if "fecha" not in caso_dict:
            caso_dict["fecha"] = datetime.now().isoformat()

        # Insertar en Mongo
        insertar_caso(caso_dict)

        return {"mensaje": "Caso creado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear caso: {e}")

# ---    
     
    # UTILIZAR CASO EXISTENTE PARA PEDIR VEREDICTO
    # Endpoint para usar un caso y pedir un veredicto
@router.post("/casos/{caso_id}/usar", response_model=AnswerResponse)
async def usar_caso(caso_id: str):
    try:
        # 1. Buscar el caso en la colección 'casos'
        casos_collection = db["casos"]
        caso = casos_collection.find_one({"_id": ObjectId(caso_id)})

        if not caso:
            raise HTTPException(status_code=404, detail="Caso no encontrado")

        # 2. Obtener el archivo (partePolicial) desde el campo 'evidencia'
        evidencia_bytes = caso.get("partePolicial")
        if not evidencia_bytes:
            raise HTTPException(status_code=400, detail="El caso no tiene archivo de evidencia")

        # 3. Guardar temporalmente el archivo para extraer el texto
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(evidencia_bytes)
            tmp_path = tmp.name

        # 4. Extraer texto del PDF
        texto = extract_text_from_pdf(tmp_path)

        # 5. Crear vectorstore temporal y lanzar consulta
        vectorstore = TemporaryVectorStoreBuilder().build(texto)
        cadena_qa = build_qa_chain([vectorstore])

        # 6. Invocar la cadena de QA con la pregunta
        resultado = cadena_qa.invoke({"query": "¿Cuál es el veredicto para este caso según el parte policial?"})
        respuesta = resultado.get("result", "No se pudo generar el veredicto.")

        # 7. Actualizar el caso con el veredicto
        return {
            "answer": respuesta,
            "sources": []  # puedes agregar fuentes reales si las tienes
        }


    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el caso: {e}")


######################################################################################################################

#ENDPOINT: Datos resumidos para dashboard principal
class CasoDashboard(BaseModel):
    id: str
    tipoDelito: str
    fecha: str

# --- ENDPOINTS PARA OBTENER DATOS DEL DASHBOARD ---
@router.get("/casos/dashboard", response_model=List[CasoDashboard])
async def obtener_casos_dashboard():
    try:
    
        collection = db["casos"]
        resultados = collection.find({}, {"_id": 1, "tipoDelito": 1, "fecha": 1})
        casos = []

        # Iterar sobre los resultados y construir la lista de casos
        for doc in resultados:
            casos.append({
                "id": str(doc["_id"]),
                "tipoDelito": doc.get("tipoDelito", "Otros"),
                "fecha": doc.get("fecha", "Sin fecha")
            })
        return casos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener casos: {e}")
    
    
# --- ENDPOINTS PARA ARMAR JSON DE LOS DASHBOARDS ---
# ENDPOINT: Datos para construir gráficas del dashboard

@router.get("/casos/dashboard-data")
async def dashboard_data():
    try:
        casos = db["casos"].find({}, {"tipoDelito": 1, "fecha": 1})

        total = 0
        tipo_count = defaultdict(int)
        mensual = defaultdict(lambda: defaultdict(int))  # tipo → mes → count

        # Recorrer los casos y acumular datos
        for caso in casos:
            total += 1

            tipo = caso.get("tipoDelito", "Otros")
            fecha = caso.get("fecha", "")

            tipo = tipo if tipo in ["Robo", "Fraude"] else "Otros"
            tipo_count[tipo] += 1

            try:
                mes = fecha[:7]  # yyyy-mm
                mensual[tipo][mes] += 1
            except:
                continue

        # Pie chart
        tiposDelito = [{"tipo": tipo, "value": count} for tipo, count in tipo_count.items()]

        # Barras más frecuentes
        barras = sorted(tiposDelito, key=lambda x: x["value"], reverse=True)[:4]
        barrasFrecuentes = [{
            "tipo": b["tipo"],
            "porcentaje": round((b["value"] / total) * 100) if total else 0
        } for b in barras]

        # Línea temporal
        todos_meses = sorted({mes for t in mensual.values() for mes in t})
        lineas = {
            "meses": todos_meses,
            "tipos": {
                tipo: [mensual[tipo].get(m, 0) for m in todos_meses]
                for tipo in ["Robo", "Fraude", "Otros"]
            }
        }

        # Retornar el JSON con los datos del dashboard
        return {
            "totalCasos": total,
            "tiposDelito": tiposDelito,
            "barrasFrecuentes": barrasFrecuentes,
            "lineasMes": lineas
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))