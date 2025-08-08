"""
Endpoints de la API para la plataforma de noticias
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, List
import logging

from agent.langgraph_agent import NewsAgent

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/get-news")
async def get_news(filter_type: str = "both") -> Dict:
    """
    Obtiene noticias filtradas de IA y Marketing
    
    Args:
        filter_type: Tipo de filtro ('ai', 'marketing', 'both')
    
    Returns:
        JSON con las noticias filtradas
    """
    try:
        logger.info(f"Solicitando noticias con filtro: {filter_type}")
        
        # Crear instancia del agente
        agent = NewsAgent()
        
        # Obtener noticias según el filtro
        if filter_type.lower() == "ai":
            query = "artificial intelligence"
        elif filter_type.lower() == "marketing":
            query = "marketing"
        else:  # both
            query = "artificial intelligence AND marketing"
        
        # Ejecutar el agente para obtener noticias
        news_data = await agent.get_filtered_news(query)
        
        logger.info(f"Obtenidas {len(news_data)} noticias")
        
        return {
            "status": "success",
            "filter": filter_type,
            "count": len(news_data),
            "news": news_data
        }
        
    except Exception as e:
        logger.error(f"Error al obtener noticias: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )

@router.get("/status")
async def api_status() -> Dict:
    """Verificar estado de la API"""
    return {
        "status": "active",
        "message": "API de noticias funcionando correctamente"
    }
