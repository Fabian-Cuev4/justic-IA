#PATH: backend/app/config/settings.py

import os
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

# URI de conexión a la base de datos MongoDB Atlas
MONGO_URI = os.getenv("MONGO_URI")

# Clave API para acceder a Gemini (usada actualmente)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configuración de Backblaze B2 (almacenamiento en la nube)
B2_KEY_ID = os.getenv("B2_KEY_ID")
B2_APP_KEY = os.getenv("B2_APP_KEY")
B2_BUCKET_NAME = os.getenv("B2_BUCKET_NAME")
