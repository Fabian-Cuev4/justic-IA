#PATH: backend/app/scripts/init_index.py

# Script para limpiar y regenerar un índice vectorial global desde los archivos PDF en Backblaze B2
from app.loaders.b2_loader import list_all_files, download_file_from_b2
from app.loaders.pdf_loader import extract_text_from_pdf
from app.vectorstore.faiss_handler import create_or_load_vectorstore, delete_vectorstore
from langchain.docstore.document import Document
import os

# Función principal: inicializar el índice vectorial global
def inicializar_indice():
    print("Inicializando índice vectorial...")

    filenames = list_all_files()                    # Lista de archivos en el bucket de Backblaze
    docs = []                                       # Lista para almacenar documentos procesados

    # Procesar cada archivo PDF
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

# Punto de entrada del script
if __name__ == "__main__":
    inicializar_indice()
