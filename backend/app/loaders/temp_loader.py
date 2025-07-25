#PATH: backend/app/loaders/temp_loader.py

from typing import List
from fastapi import UploadFile
import fitz  # PyMuPDF

# Clase responsable de cargar archivos PDF temporales (sin guardarlos en disco)
class TempDocumentLoader:
    def __init__(self, upload_file: UploadFile):
        self.upload_file = upload_file                                  # Constructor de la clase

    async def extract_text(self) -> str:
        # Extrae texto plano desde el archivo PDF cargado por el usuario.

        contents = await self.upload_file.read()
        pdf = fitz.open(stream=contents, filetype="pdf")
        text = ""
        
        # Itera sobre cada página del PDF y extrae el texto.
        for page in pdf:
            text += page.get_text()
        pdf.close()
        
        return text
