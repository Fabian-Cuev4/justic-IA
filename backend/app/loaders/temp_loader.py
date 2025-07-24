# 7) backend/app/loaders/temp_loader.py

from typing import List
from fastapi import UploadFile
import fitz  # PyMuPDF

# es responsable de extraer el texto plano desde el archivo PDF cargado por el usuario. PyMuPDF
class TempDocumentLoader:
    def __init__(self, upload_file: UploadFile):
        self.upload_file = upload_file

    async def extract_text(self) -> str:
        contents = await self.upload_file.read()
        pdf = fitz.open(stream=contents, filetype="pdf")
        text = ""
        for page in pdf:
            text += page.get_text()
        pdf.close()
        return text
