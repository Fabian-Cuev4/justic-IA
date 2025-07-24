# backend/app/config/settings.py

import os
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

# MongoDB Atlas
MONGO_URI = os.getenv("MONGO_URI")

# OpenAI / Gemini
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Backblaze B2
B2_KEY_ID = os.getenv("B2_KEY_ID")
B2_APP_KEY = os.getenv("B2_APP_KEY")
B2_BUCKET_NAME = os.getenv("B2_BUCKET_NAME")
