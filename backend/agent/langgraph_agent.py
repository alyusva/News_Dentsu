"""
Agente LangGraph para obtener y filtrar noticias de IA y Marketing
"""

import os
import requests
import json
from typing import List, Dict, Any
from datetime import datetime
import logging

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langgraph.graph import Graph
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsAgent:
    """Agente para obtener y filtrar noticias usando LangGraph + OpenAI"""
    
    def __init__(self):
        self.news_api_key = os.getenv("NEWS_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        if not self.news_api_key:
            raise ValueError("NEWS_API_KEY no encontrada en las variables de entorno")
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY no encontrada en las variables de entorno")
        
        # Inicializar modelo OpenAI
        self.llm = ChatOpenAI(
            api_key=self.openai_api_key,
            model="gpt-4",
            temperature=0.3
        )
        
        # Crear el grafo de LangGraph
        self.graph = self._create_langgraph()
    
    def _create_langgraph(self) -> Graph:
        """Crear el grafo de procesamiento con LangGraph"""
        graph = Graph()
        
        # Nodos del grafo
        graph.add_node("fetch_news", self._fetch_news_from_api)
        graph.add_node("filter_news", self._filter_relevant_news)
        graph.add_node("summarize_news", self._summarize_with_openai)
        
        # Edges del grafo
        graph.add_edge("fetch_news", "filter_news")
        graph.add_edge("filter_news", "summarize_news")
        
        # Punto de entrada
        graph.set_entry_point("fetch_news")
        
        return graph.compile()
    
    async def get_filtered_news(self, query: str) -> List[Dict[str, Any]]:
        """
        Ejecutar el pipeline completo para obtener noticias filtradas
        
        Args:
            query: Consulta de búsqueda para las noticias
            
        Returns:
            Lista de noticias filtradas y resumidas
        """
        try:
            logger.info(f"Iniciando búsqueda de noticias con query: {query}")
            
            # Ejecutar el grafo
            result = await self.graph.ainvoke({"query": query})
            
            return result.get("processed_news", [])
            
        except Exception as e:
            logger.error(f"Error en el agente de noticias: {str(e)}")
            return []
    
    def _fetch_news_from_api(self, state: Dict) -> Dict:
        """Nodo 1: Obtener noticias desde NewsAPI"""
        query = state["query"]
        
        try:
            # Configurar parámetros de la API
            url = "https://newsapi.org/v2/everything"
            params = {
                "q": query,
                "language": "en",
                "sortBy": "publishedAt",
                "pageSize": 20,  # Limitar a 20 noticias
                "apiKey": self.news_api_key
            }
            
            logger.info(f"Consultando NewsAPI con query: {query}")
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            articles = data.get("articles", [])
            
            logger.info(f"Obtenidos {len(articles)} artículos de NewsAPI")
            
            state["raw_news"] = articles
            return state
            
        except Exception as e:
            logger.error(f"Error al obtener noticias de la API: {str(e)}")
            state["raw_news"] = []
            return state
    
    def _filter_relevant_news(self, state: Dict) -> Dict:
        """Nodo 2: Filtrar noticias relevantes"""
        raw_news = state.get("raw_news", [])
        
        filtered_news = []
        
        for article in raw_news:
            title = article.get("title", "")
            description = article.get("description", "")
            content = article.get("content", "")
            
            # Filtro básico: debe contener palabras clave
            text_to_check = f"{title} {description} {content}".lower()
            
            # Verificar si contiene términos relacionados con IA y/o Marketing
            ai_terms = ["artificial intelligence", "ai", "machine learning", "deep learning", "neural network"]
            marketing_terms = ["marketing", "advertising", "campaign", "brand", "customer"]
            
            has_ai = any(term in text_to_check for term in ai_terms)
            has_marketing = any(term in text_to_check for term in marketing_terms)
            
            # Incluir si tiene al menos uno de los temas
            if has_ai or has_marketing:
                # Clasificar el artículo
                if has_ai and has_marketing:
                    category = "both"
                elif has_ai:
                    category = "ai"
                else:
                    category = "marketing"
                
                filtered_article = {
                    "title": title,
                    "description": description,
                    "url": article.get("url"),
                    "urlToImage": article.get("urlToImage"),
                    "publishedAt": article.get("publishedAt"),
                    "source": article.get("source", {}).get("name"),
                    "category": category
                }
                
                filtered_news.append(filtered_article)
        
        logger.info(f"Filtradas {len(filtered_news)} noticias relevantes")
        
        state["filtered_news"] = filtered_news
        return state
    
    def _summarize_with_openai(self, state: Dict) -> Dict:
        """Nodo 3: Resumir noticias con OpenAI"""
        filtered_news = state.get("filtered_news", [])
        
        processed_news = []
        
        for article in filtered_news:
            try:
                # Si la descripción es muy larga, resumirla
                description = article.get("description", "")
                
                if len(description) > 200:
                    # Crear prompt para resumir
                    messages = [
                        SystemMessage(content="""Eres un experto en resumir noticias. 
                        Crea un resumen conciso y claro de máximo 150 caracteres que capture 
                        los puntos clave de la noticia."""),
                        HumanMessage(content=f"Resumir esta noticia: {description}")
                    ]
                    
                    # Obtener resumen de OpenAI
                    response = self.llm.invoke(messages)
                    summary = response.content.strip()
                else:
                    summary = description
                
                # Preparar artículo procesado
                processed_article = {
                    "title": article["title"],
                    "description": summary,
                    "url": article["url"],
                    "image": article["urlToImage"] or "/api/placeholder/300/200",
                    "publishedAt": article["publishedAt"],
                    "source": article["source"],
                    "category": article["category"]
                }
                
                processed_news.append(processed_article)
                
            except Exception as e:
                logger.warning(f"Error al procesar artículo: {str(e)}")
                # Usar el artículo sin procesar si hay error
                processed_article = {
                    "title": article["title"],
                    "description": article.get("description", ""),
                    "url": article["url"],
                    "image": article["urlToImage"] or "/api/placeholder/300/200",
                    "publishedAt": article["publishedAt"],
                    "source": article["source"],
                    "category": article["category"]
                }
                processed_news.append(processed_article)
        
        logger.info(f"Procesados {len(processed_news)} artículos finales")
        
        state["processed_news"] = processed_news
        return state

# Función auxiliar para testing
async def test_agent():
    """Función de prueba para el agente"""
    try:
        agent = NewsAgent()
        news = await agent.get_filtered_news("artificial intelligence AND marketing")
        print(f"Obtenidas {len(news)} noticias:")
        for article in news[:3]:  # Mostrar solo las primeras 3
            print(f"- {article['title']}")
        return news
    except Exception as e:
        print(f"Error en test: {str(e)}")
        return []

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_agent())
