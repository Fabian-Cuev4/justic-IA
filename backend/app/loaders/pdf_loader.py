# 9) backend/app/loaders/pdf_loader.py

import fitz                                                     # PyMuPDF, leer páginas de un PDF y extraer su contenido como texto plano.

def extract_text_from_pdf(file_path: str) -> str:
    """Extraigo texto plano de un archivo PDF usando PyMuPDF."""
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    # Devuelve el texto extraído del PDF en una sola cadena.
    return text
