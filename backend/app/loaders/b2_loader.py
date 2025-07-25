#PATH: backend/app/loaders/b2_loader.py

import os
import tempfile
from b2sdk.v2 import InMemoryAccountInfo, B2Api
from app.config.settings import B2_KEY_ID, B2_APP_KEY, B2_BUCKET_NAME

# Autentica mi cuenta Backblaze y obtiene acceso al bucket especificado.
info = InMemoryAccountInfo()                                                # Crea una instancia de información de cuenta en memoria (sin persistencia en disco)
b2_api = B2Api(info)                                                        # Crea una instancia de la API de Backblaze 
b2_api.authorize_account("production", B2_KEY_ID, B2_APP_KEY)
bucket = b2_api.get_bucket_by_name(B2_BUCKET_NAME)

# Descarga un archivo específico desde Backblaze B2 y lo guarda en el directorio temporal local
def download_file_from_b2(filename: str) -> str:
    """
    Descarga un archivo desde Backblaze a un directorio local.
    """
    temp_dir = tempfile.gettempdir()
    local_path = os.path.join(temp_dir, filename)
    downloaded_file = bucket.download_file_by_name(filename)
    downloaded_file.save_to(local_path)
    return local_path

# Devuelve una lista de los nombres de todos los archivos del bucket (prueba de funcionamiento).
def list_all_files() -> list:
    """
    Lista todos los nombres de archivos en el bucket de Backblaze.
    """
    file_names = []
    for file_info, _ in bucket.ls():
        file_names.append(file_info.file_name)
    return file_names
