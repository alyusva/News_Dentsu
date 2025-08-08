"""
Aplicación principal para HuggingFace Spaces
Plataforma de Noticias IA y Marketing - Dentsu
"""

import gradio as gr
import subprocess
import threading
import time
import os
import signal
import requests
from pathlib import Path

# Configurar variables de entorno desde Spaces
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")
os.environ["NEWS_API_KEY"] = os.getenv("NEWS_API_KEY", "")
os.environ["HOST"] = "0.0.0.0"
os.environ["PORT"] = "7860"

class AppManager:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        
    def start_backend(self):
        """Iniciar el servidor FastAPI"""
        try:
            # Cambiar al directorio backend
            backend_dir = Path(__file__).parent / "backend"
            
            # Iniciar FastAPI en puerto 8000
            self.backend_process = subprocess.Popen(
                ["python", "main.py"],
                cwd=backend_dir,
                env=os.environ.copy()
            )
            print("✅ Backend iniciado en puerto 8000")
            return True
        except Exception as e:
            print(f"❌ Error iniciando backend: {e}")
            return False
    
    def start_frontend(self):
        """Preparar el frontend (build estático)"""
        try:
            frontend_dir = Path(__file__).parent / "frontend"
            
            # Instalar dependencias
            subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
            
            # Build del frontend
            subprocess.run(["npm", "run", "build"], cwd=frontend_dir, check=True)
            
            print("✅ Frontend construido exitosamente")
            return True
        except Exception as e:
            print(f"❌ Error construyendo frontend: {e}")
            return False
    
    def stop_services(self):
        """Detener todos los servicios"""
        if self.backend_process:
            self.backend_process.terminate()
            self.backend_process = None
        
        if self.frontend_process:
            self.frontend_process.terminate()
            self.frontend_process = None

# Instancia global del manager
app_manager = AppManager()

def check_backend_health():
    """Verificar si el backend está funcionando"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_news_from_backend(filter_type="both"):
    """Obtener noticias del backend"""
    try:
        response = requests.get(
            f"http://localhost:8000/api/get-news?filter_type={filter_type}",
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get("news", [])
        else:
            return []
    except Exception as e:
        print(f"Error obteniendo noticias: {e}")
        return []

def format_news_for_display(news_list):
    """Formatear noticias para mostrar en Gradio"""
    if not news_list:
        return "❌ No se encontraron noticias. Verifica la configuración de API keys."
    
    formatted_news = []
    
    for i, article in enumerate(news_list, 1):
        title = article.get("title", "Sin título")
        description = article.get("description", "Sin descripción")
        url = article.get("url", "#")
        source = article.get("source", "Fuente desconocida")
        category = article.get("category", "general")
        
        # Formatear categoría
        if category == "both":
            category_text = "🤖📈 IA + Marketing"
        elif category == "ai":
            category_text = "🤖 Inteligencia Artificial"
        else:
            category_text = "📈 Marketing"
        
        news_item = f"""
### {i}. {title}

**Categoría:** {category_text}  
**Fuente:** {source}

{description}

[🔗 Leer artículo completo]({url})

---
"""
        formatted_news.append(news_item)
    
    return "\n".join(formatted_news)

def fetch_and_display_news(filter_type):
    """Función principal para obtener y mostrar noticias"""
    if not check_backend_health():
        return "❌ Backend no disponible. Iniciando servicios..."
    
    news = get_news_from_backend(filter_type)
    return format_news_for_display(news)

def initialize_app():
    """Inicializar la aplicación"""
    print("🚀 Iniciando Plataforma de Noticias IA y Marketing...")
    
    # Iniciar backend
    success = app_manager.start_backend()
    
    if success:
        # Esperar a que el backend esté listo
        print("⏳ Esperando a que el backend esté listo...")
        for i in range(30):  # Esperar máximo 30 segundos
            if check_backend_health():
                print("✅ Backend listo!")
                break
            time.sleep(1)
        else:
            print("⚠️ Backend tardó demasiado en iniciarse")
    
    return success

# Inicializar la aplicación al importar
print("🔧 Configurando aplicación...")
initialize_app()

# Crear interfaz de Gradio
with gr.Blocks(
    title="Plataforma de Noticias IA y Marketing",
    theme=gr.themes.Soft(),
    css="""
    .container { max-width: 1200px; margin: 0 auto; }
    .news-container { max-height: 600px; overflow-y: auto; }
    """
) as demo:
    
    gr.Markdown("""
    # 🤖📰 Plataforma de Noticias IA y Marketing
    
    ## Prueba Técnica - Dentsu
    
    Esta plataforma utiliza agentes de IA para obtener y filtrar noticias relacionadas con 
    **Inteligencia Artificial** y **Marketing Digital** desde múltiples fuentes.
    
    ### Características:
    - 🔍 Filtrado inteligente con LangGraph + OpenAI
    - 📊 Categorización automática de contenido
    - 🌐 Noticias en tiempo real desde NewsAPI
    - 🎯 Resúmenes optimizados para cada área
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            filter_dropdown = gr.Dropdown(
                choices=[
                    ("Ambos (IA + Marketing)", "both"),
                    ("Solo Inteligencia Artificial", "ai"),
                    ("Solo Marketing", "marketing")
                ],
                value="both",
                label="🔍 Filtro de Noticias",
                info="Selecciona el tipo de noticias que deseas ver"
            )
            
            fetch_button = gr.Button(
                "🔄 Obtener Noticias",
                variant="primary",
                size="lg"
            )
            
            gr.Markdown("""
            ### ℹ️ Información del Sistema
            - **Backend:** FastAPI + LangGraph
            - **IA:** OpenAI GPT-4
            - **Fuente:** NewsAPI
            - **Estado:** 🟢 Activo
            """)
        
        with gr.Column(scale=3):
            news_output = gr.Markdown(
                value="👆 Selecciona un filtro y presiona 'Obtener Noticias' para comenzar",
                label="📰 Noticias Encontradas",
                elem_classes=["news-container"]
            )
    
    # Event handlers
    fetch_button.click(
        fn=fetch_and_display_news,
        inputs=[filter_dropdown],
        outputs=[news_output],
        show_progress=True
    )
    
    # Auto-load inicial
    demo.load(
        fn=lambda: fetch_and_display_news("both"),
        outputs=[news_output],
        show_progress=True
    )
    
    gr.Markdown("""
    ---
    
    **Desarrollado para Dentsu** | Prueba Técnica 2024  
    Tecnologías: React, FastAPI, LangGraph, OpenAI, NewsAPI
    """)

# Cleanup al cerrar
def cleanup():
    app_manager.stop_services()

import atexit
atexit.register(cleanup)

if __name__ == "__main__":
    # Configurar para HuggingFace Spaces
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=True
    )
