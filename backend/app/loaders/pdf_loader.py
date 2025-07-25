#PATH: backend/app/loaders/pdf_loader.py

import fitz                                                     # PyMuPDF, leer páginas de un PDF y extraer su contenido como texto plano.

# Extrae texto plano desde un archivo PDF utilizando PyMuPDF.
def extract_text_from_pdf(file_path: str) -> str:
    
    text = ""
    
    # Abre el archivo PDF y recorre cada página para extraer su texto.
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    # Devuelve el texto extraído del PDF en una sola cadena.
    return text
