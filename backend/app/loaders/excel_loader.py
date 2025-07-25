
#PATH: backend/app/loaders/excel_loader.py

import pandas as pd

# Función para extraer texto de un archivo Excel
def extract_text_from_excel(file_path: str) -> str:                         # Combina todas las hojas y celdas en un solo string separado por saltos de línea.
 
    try:
        xl = pd.ExcelFile(file_path)
        all_text = []

        # Iterar sobre cada hoja del archivo
        for sheet in xl.sheet_names:
            df = xl.parse(sheet)
            text = df.astype(str).fillna("").values.flatten().tolist()
            all_text.append("\\n".join(text))

        return "\\n".join(all_text)

    except Exception as e:
        print(f"Error al procesar archivo Excel: {file_path} -> {e}")
        return ""
 