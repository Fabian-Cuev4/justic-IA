 
# ⚖️ JusticIA — Plataforma Judicial Inteligente

JusticIA es una plataforma web que simula el rol de un juez asistido por inteligencia artificial. Permite analizar denuncias, partes policiales y documentos legales utilizando modelos avanzados de lenguaje y recuperación aumentada (RAG), con el objetivo de emitir dictámenes jurídicos automatizados basados en la legislación ecuatoriana.

## 🚀 Tecnologías Utilizadas

### Backend (Python)
- FastAPI
- LangChain
- Google Gemini API
- HuggingFace (MiniLM)
- FAISS
- PyMuPDF
- b2sdk
- MongoDB Atlas
- dotenv

### Frontend (Angular + TailwindCSS)
- Angular
- TailwindCSS

## 📂 Estructura del Proyecto

justicIA/
├── backend/
│   ├── app/
│   │   ├── config/
│   │   ├── core/
│   │   ├── db/
│   │   ├── loaders/
│   │   ├── llm/
│   │   └── main.py
├── frontend/
├── requirements.txt
└── .env

## 🛠️ Instalación

### Backend

```bash
git clone https://github.com/Fabian-Cuev4/justicIA.git
cd justicIA/backend
python -m venv venv
source venv/bin/activate
pip install -r ../requirements.txt
```

Variables en `.env`:

```env
GOOGLE_API_KEY=...
HUGGINGFACEHUB_API_TOKEN=...
MONGO_URL=...
B2_KEY_ID=...
B2_APPLICATION_KEY=...
B2_BUCKET_NAME=...
```

### Frontend

```bash
cd justicIA/frontend
npm install
ng serve
```

## ▶️ Ejecución del servidor

### Backend (FastAPI)
```
uvicorn app.main:app --reload
```

### Frontend (Angular)
```
ng serve
```

## 🤖 Cómo funciona JusticIA

1. Subida de documentos legales
2. Procesamiento y vectorización (LangChain + FAISS)
3. Consulta legal con contexto (Gemini + leyes en Backblaze)
4. Generación de dictamen legal

## 📊 Características clave

- Múltiples sesiones
- Clasificación de delitos
- Veredictos automáticos
- Dashboard estadístico
- MongoDB + Backblaze integrados

## 🧪 Ejemplo de uso (Postman)

1. POST /upload-query (archivo temporal)
2. POST /query (consulta legal general)

## 👨‍💻 Autores

- Fabian Cueva
- Bryan Chileno
- Abel Navarrete
- Kuntur Security 🦅

## 📜 Licencia

MIT License
 