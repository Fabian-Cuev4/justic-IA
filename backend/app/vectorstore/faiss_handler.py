# 5) backend/app/vectorstore/faiss_handler.py

import os
from langchain.text_splitter import RecursiveCharacterTextSplitter          # Divide el texto en chunks
from langchain_community.vectorstores import FAISS                          # Motor de búsqueda vectorial
from langchain_huggingface import HuggingFaceEmbeddings            # Convierte texto en vectores
from langchain.docstore.document import Document                            # Envuelve texto en un formato estructurado  
from typing import Union, List
import shutil


# Define la carpeta donde se guardarán los índices y la crea si no existe.
FAISS_DIR = "faiss_indexes"
os.makedirs(FAISS_DIR, exist_ok=True)

# se divide el texto (en bloques de 1000 caracteres con 100 de solapamiento). Se convierte cada parte en un vector (embedding).
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ".", " ", ""]
)

embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Carga un índice FAISS existente si ya fue creado.
def create_or_load_vectorstore(data: Union[str, List[Document]], index_name: str) -> FAISS:
    index_path = os.path.join(FAISS_DIR, index_name)
    index_faiss = os.path.join(index_path, "index.faiss")
    index_pkl = os.path.join(index_path, "index.pkl")

    # Solo cargar si los dos archivos existen
    if os.path.exists(index_faiss) and os.path.exists(index_pkl):
        return FAISS.load_local(index_path, embeddings=embedder, allow_dangerous_deserialization=True)

    # Crear desde cero
    if isinstance(data, str):
        docs = [Document(page_content=chunk) for chunk in text_splitter.split_text(data)]
    elif isinstance(data, list):
        docs = data
    else:
        raise ValueError("El parámetro `data` debe ser un string o una lista de Document.")

    # ✅ Asegura que el directorio exista antes de guardar el índice
    os.makedirs(index_path, exist_ok=True)

    print(f"Total de chunks creados: {len(docs)}")          # Solo para depuración
    vectorstore = FAISS.from_documents(docs, embedder)
    vectorstore.save_local(index_path)
    return vectorstore

def delete_vectorstore(index_name: str):
    index_path = os.path.join(FAISS_DIR, index_name)
    if os.path.exists(index_path):
        shutil.rmtree(index_path)
        

