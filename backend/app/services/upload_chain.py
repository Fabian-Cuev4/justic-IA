# 4) backend/app/services/upload_chain.py

from app.loaders.temp_loader import TempDocumentLoader
from app.vectorstore.temp_vectorstore import TemporaryVectorStoreBuilder
from app.vectorstore.faiss_handler import create_or_load_vectorstore
from app.loaders.b2_loader import list_all_files, download_file_from_b2
from app.loaders.pdf_loader import extract_text_from_pdf
from app.llm.rag_chain import build_qa_chain
from langchain.vectorstores.base import VectorStore
from fastapi import UploadFile

# Guarda el archivo cargado por el usuario como atributo.
class UploadQAService:
    def __init__(self, upload_file: UploadFile):
        self.upload_file = upload_file

    async def get_answer(self, question: str):          # Elimina el tipo de retorno (para permitir devolver 2 cosas)
        file_bytes = await self.upload_file.read()      # Leer bytes del archivo original
        self.upload_file.file.seek(0)

        # 1. Extraer texto del archivo temporal
        loader = TempDocumentLoader(self.upload_file)
        text = await loader.extract_text()

        # 2. Crear vectorstore temporal desde el texto del caso
        temp_vectorstore = TemporaryVectorStoreBuilder().build(text)

        # 3. Cargar vectorstore persistente (leyes en Backblaze)
        filenames = list_all_files()
        all_text = ""
        for fname in filenames:
            if fname.endswith(".pdf"):
                local_path = download_file_from_b2(fname)
                text = extract_text_from_pdf(local_path)
                all_text += f"\n{text}"

        legal_vectorstore: VectorStore = create_or_load_vectorstore(all_text, index_name="global_index")

        # 4. Combinar ambos contextos (temporal + legal)
        qa_chain = build_qa_chain([temp_vectorstore, legal_vectorstore])

        # 5. Obtener respuesta
        result = qa_chain.invoke({"query": question})
        answer = result.get("result", str(result)) if isinstance(result, dict) else result

        return answer, file_bytes  # Devuelve ambos valores
