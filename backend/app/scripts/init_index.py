# backend/app/scripts/init_index.py
#LIMPIA

from app.loaders.b2_loader import list_all_files, download_file_from_b2
from app.loaders.pdf_loader import extract_text_from_pdf
from app.vectorstore.faiss_handler import create_or_load_vectorstore, delete_vectorstore
from langchain.docstore.document import Document
import os

def inicializar_indice():
    print("Inicializando índice vectorial...")

    filenames = list_all_files()
    docs = []

    for fname in filenames:
        if fname.endswith(".pdf"):
            print(f"Procesando: {fname}")
            local_path = download_file_from_b2(fname)
            text = extract_text_from_pdf(local_path)
            docs.append(Document(page_content=text, metadata={"source": fname}))

    # Eliminar cualquier índice viejo
    delete_vectorstore("global_index")

    # Crear nuevo índice desde cero
    create_or_load_vectorstore(docs, index_name="global_index")
    print("✅ Índice global creado correctamente.")

if __name__ == "__main__":
    inicializar_indice()
