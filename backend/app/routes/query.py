#PATH: backend/app/routes/query.py

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from app.loaders.b2_loader import list_all_files, download_file_from_b2
from app.loaders.pdf_loader import extract_text_from_pdf 
from app.loaders.excel_loader import extract_text_from_excel
from app.vectorstore.faiss_handler import create_or_load_vectorstore
from app.llm.rag_chain import build_qa_chain
from app.services.upload_chain import UploadQAService
from pathlib import Path
import re
from app.db.mongo import guardar_respuesta
from app.core.session import get_session_id
from typing import List


router = APIRouter()

# Modelos de datos para las solicitudes y respuestas
class QuestionRequest(BaseModel):
    question: str                   # Pregunta que el usuario quiere hacer
    filename: str                   # Campo incluido por compatibilidad, actualmente no se usa

class AnswerResponse(BaseModel):
    answer: str                     # Respuesta generada por la IA
    sources: List[str]              # Fuentes de donde se obtuvo la información  
    

# Consulta usando todos los documentos persistentes en B2, vectorizados individualmente
@router.post("/query", response_model=AnswerResponse)
async def query_doc(data: QuestionRequest):
    try:
        filenames = list_all_files()
        sources = [fname for fname in filenames if fname.endswith(".pdf") or fname.endswith(".xlsx")]
        vectorstores = []

        for fname in sources:
            local_path = download_file_from_b2(fname)

            if fname.endswith(".pdf"):
                text = extract_text_from_pdf(local_path)
            elif fname.endswith(".xlsx"):
                text = extract_text_from_excel(local_path)
            else:
                continue  # Por seguridad, omitir si no es compatible
            
            # Nombre de índice seguro    
            safe_name = re.sub(r'[^\w\d_-]', '_', Path(fname).stem)                   # Reemplazar caracteres no seguros
            index_name = safe_name[:50]
            
            # Crear o cargar el vectorstore
            vs = create_or_load_vectorstore(text, index_name=index_name)
            vectorstores.append(vs)

        # Construye la cadena de preguntas y respuestas con todos los índices
        qa_chain = build_qa_chain(vectorstores)
        result = qa_chain.invoke({"query": data.question})

        answer = result.get("result", str(result)) if isinstance(result, dict) else result

        guardar_respuesta(
            question=data.question,
            answer=answer,
            sources=sources,
            session_id=get_session_id()
        )

        return {"answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ENDPOINT: Consulta con archivo temporal
@router.post("/upload-query", response_model=AnswerResponse)
async def upload_query(question: str = Form(...), file: UploadFile = File(...)):
    try:
        service = UploadQAService(upload_file=file)

        # Método que devuelve respuesta + archivo
        answer, file_bytes = await service.get_answer(question)

        # Guarda la consulta y el archivo original en MongoDB
        guardar_respuesta(
            question=question,
            answer=answer,
            sources=[file.filename],
            session_id=get_session_id(),
            file_bytes=file_bytes
        )

        return {"answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


##################################################################################################################

# ENDPOINT: Consulta con todos los documentos (alternativa simplificada)

@router.post("/preguntar", response_model=AnswerResponse)                       # El formato de respuesta puede cambiar si se requiere
async def preguntar_simple(data: QuestionRequest):
    try:
        # Lista todos los archivos .pdf y .xlsx disponibles en B2
        archivos = list_all_files()
        fuentes = [f for f in archivos if f.endswith(".pdf") or f.endswith(".xlsx")]

        vectorstores = []
        # Procesa cada archivo, extrae texto y crea un vectorstore
        for archivo in fuentes:
            local_path = download_file_from_b2(archivo)

            if archivo.endswith(".pdf"):
                texto = extract_text_from_pdf(local_path)
            elif archivo.endswith(".xlsx"):
                texto = extract_text_from_excel(local_path)
            else:
                continue

            from pathlib import Path
            import re
            nombre_base = re.sub(r'[^\w\d_-]', '_', Path(archivo).stem)
            nombre_indice = nombre_base[:50]

            vs = create_or_load_vectorstore(texto, index_name=nombre_indice)
            vectorstores.append(vs)

        # Construye cadena de preguntas y respuestas con todos los índices
        cadena_qa = build_qa_chain(vectorstores)
        resultado = cadena_qa.invoke({"query": data.question})

        respuesta = resultado.get("result", "No se encontró respuesta.")
        return {"answer": respuesta}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al responder: {e}")

"""
    Versión alternativa del endpoint que también procesa todos los archivos
    PDF y Excel persistentes, construye vectores y lanza la consulta.
    
"""

 