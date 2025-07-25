#PATH: backend/app/vectorstore/temp_vectorstore.py

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.docstore.document import Document

# toma un texto plano y lo convierte en un índice FAISS temporal que no se guarda en disco.
class TemporaryVectorStoreBuilder:
    # Inicializa la clase cargando el modelo de embeddings de HuggingFace.
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Método para construir un vectorstore temporal a partir de un texto plano.
    def build(self, text: str) -> FAISS:
        # Convertir el texto plano en un documento LangChain
        documents = [Document(page_content=text)]
        # Crear vectorstore temporal
        vectorstore = FAISS.from_documents(documents, self.embeddings)
        return vectorstore
