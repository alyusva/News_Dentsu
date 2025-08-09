"""
Plataforma de Noticias IA y Marketing - Dentsu
Servidor local de desarrollo con configuración optimizada
"""

import uvicorn
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el directorio padre
load_dotenv("../.env")

if __name__ == "__main__":
    print("🚀 Iniciando servidor local de desarrollo...")
    print("📡 Backend URL: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    
    uvicorn.run(
        "app.main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=True,  # Auto-reload en desarrollo
        log_level="info"
    )
