"""
Aplicación FastAPI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv("../.env")

# Importar rutas
from api.endpoints import router

# Crear instancia de FastAPI
app = FastAPI(
    title="Plataforma de Noticias IA y Marketing",
    description="API para obtener y filtrar noticias de Inteligencia Artificial y Marketing",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {
        "message": "Plataforma de Noticias IA y Marketing - API activa",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
