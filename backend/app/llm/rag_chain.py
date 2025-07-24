# 1) backend/app/llm/rag_chain.py

from langchain_google_genai import ChatGoogleGenerativeAI           #
from app.config.settings import GEMINI_API_KEY                      #
#from langchain_community.chat_models import ChatOpenAI

from langchain.chains import RetrievalQA                                    #combina un modelo LLM con un sistema de recuperación de contexto.     

from langchain_core.prompts import PromptTemplate                           # Permite crear plantillas de prompts para el modelo LLM.
from langchain.schema import BaseRetriever                                  # Interfaz base para los recuperadores de datos.
from langchain.vectorstores.base import VectorStore
from langchain.retrievers import MergerRetriever                            # Permite combinar múltiples fuentes de recuperación de datos.

import os
from dotenv import load_dotenv

load_dotenv()

def build_qa_chain(vectorstores: list[VectorStore]) -> RetrievalQA:         # función principal del módulo basadas en fuentes vertoriales
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",                                           # gemini-2.5-flash   ////  gemini-1.5-flash
        google_api_key=GEMINI_API_KEY,
        temperature=0.3
)

# def build_qa_chain(vectorstores: list[VectorStore]) -> RetrievalQA:
#     llm = ChatOpenAI(
#         model="gpt-4-turbo",
#         temperature=0.3,
#         max_tokens=700,
#         openai_api_key=os.getenv("OPENAI_API_KEY")
#     )

    # Asegurar que sea una lista (por si solo se pasa un elemento)
    if not isinstance(vectorstores, list):
        vectorstores = [vectorstores]

    # Converte cada VectorStore a retrievers
    # retrievers = [vs.as_retriever() for vs in vectorstores]
    retrievers = [
        vs.as_retriever(search_kwargs={"k": 2})  # menos documentos por fuente
        for vs in vectorstores
    ]           

    # Combinar múltiples retrievers
    combined_retriever: BaseRetriever = MergerRetriever(retrievers=retrievers)

    # Prompt (rol) del Juez IA
    from langchain.prompts import PromptTemplate

    # Prompt (rol del Juez IA)
    prompt = PromptTemplate.from_template("""
    Eres **justicIA**, una inteligencia artificial especializada en leyes ecuatorianas que actúa como un juez.

    Debes responder la siguiente pregunta utilizando únicamente la información proporcionada en el contexto, que puede incluir:
    1. El Código Orgánico Integral Penal (COIP) y el Código Procesal Penal.
    2. Información relevante sobre centros penitenciarios del Ecuador.
    3. Documentación o evidencia legal proporcionada por el usuario.

    Con base en ese contexto, formula una **sentencia** o **dictamen judicial** claro y fundamentado:
        - Al final, entrega un **VEREDICTO DIRECTO** en una sola línea que indique:
        - Si es culpable o inocente
        - Años de condena (si aplica)
        - Nombre del centro de reclusión y pabellón o carcel (si aplica)

    Ejemplo:
    VEREDICTO DIRECTO: Culpable. Condena de 2 años. CPL Loja, Pabellón B.                                     

    - Cita los artículos del COIP u otras leyes aplicables.
    - Expón el razonamiento paso a paso (hechos → normas → conclusión).
    - Mantén un tono profesional, objetivo y prudente.
    - Si se trata de asignar un pabellón penitenciario, usa los datos disponibles en el contexto y emite una recomendación directa.
    - Si la pregunta no tiene nada que ver con justicIA, puedes responderla sin estructura si es lo más eficiente.

    Contexto legal y del caso:
    {context}

    Pregunta del usuario:
    {question}

    Respuesta razonada y fundamentada:
    """)

    # Crear la cadena de QA con el LLM y el recuperador combinado
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=combined_retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt}
    )


