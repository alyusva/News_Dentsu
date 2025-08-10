"""
Backend principal de la plataforma de noticias de IA y Marketing
Dentsu - Prueba Técnica
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Cargar variables de entorno primero
load_dotenv("../.env")

# Importar rutas después de cargar variables
from api.endpoints import router

# Crear instancia de FastAPI
app = FastAPI(
    title="Plataforma de Noticias IA y Marketing",
    description="API para obtener y filtrar noticias de Inteligencia Artificial y Marketing",
    version="1.0.0"
)

# Configurar CORS para permitir conexiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    """Endpoint de verificación de estado"""
    return {
        "message": "Plataforma de Noticias IA y Marketing - API activa",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Endpoint de verificación de salud"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    
    # Cloud Run usa la variable PORT, con fallback a 8000
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    debug = os.getenv("DEBUG", "False").lower() == "true"
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug,
        workers=1 if debug else 4  # Múltiples workers en producción
    )
