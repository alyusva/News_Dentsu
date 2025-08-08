# Plataforma de Noticias IA y Marketing - Dentsu

Esta aplicación es una prueba técnica para Dentsu que permite a los usuarios acceder a noticias recientes relacionadas con Inteligencia Artificial y Marketing. Las noticias se obtienen automáticamente desde la API de NewsAPI y se filtran usando un agente LangGraph conectado a OpenAI.

## 🚀 Características

- **Frontend moderno**: React + Vite con diseño responsive
- **Backend robusto**: FastAPI con integración de LangGraph + OpenAI
- **Filtrado inteligente**: Agente LLM para curar contenido relevante
- **Modo claro/oscuro**: Soporte completo para temas
- **Estado persistente**: LocalStorage para preferencias del usuario
- **Interfaz intuitiva**: Diseño basado en componentes de Figma

## 🏗️ Arquitectura

```
News_Dentsu/
├── frontend/           # React + Vite application
│   ├── src/
│   │   ├── components/ # Componentes UI reutilizables
│   │   ├── pages/      # Páginas principales
│   │   ├── lib/        # Utilidades
│   │   └── ...
│   └── package.json
├── backend/            # FastAPI application
│   ├── api/           # Endpoints de la API
│   ├── agent/         # Agente LangGraph
│   └── main.py        # Servidor principal
├── data/              # Logs y datos temporales
├── requirements.txt   # Dependencias Python
├── .env              # Variables de entorno
└── README.md
```

## 🛠️ Tecnologías

### Frontend
- **React 18** - Biblioteca de UI
- **Vite** - Build tool y dev server
- **Tailwind CSS** - Estilos utilitarios
- **Lucide React** - Iconos
- **React Router** - Navegación

### Backend
- **FastAPI** - Framework web moderno
- **LangGraph** - Orquestación de agentes LLM
- **OpenAI API** - Procesamiento de lenguaje natural
- **NewsAPI** - Fuente de noticias
- **Python 3.9+** - Lenguaje principal

## 📋 Prerrequisitos

- Node.js 18+ y npm/yarn
- Python 3.9+
- Claves de API:
  - OpenAI API Key
  - NewsAPI Key

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd News_Dentsu
```

### 2. Configurar variables de entorno
```bash
cp .env.example .env
```

Editar `.env` con tus claves:
```env
OPENAI_API_KEY=tu_openai_api_key_aqui
NEWS_API_KEY=tu_news_api_key_aqui
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

### 3. Configurar Backend
```bash
# Instalar dependencias Python
pip install -r requirements.txt

# Ejecutar servidor de desarrollo
cd backend
python main.py
```

El backend estará disponible en `http://localhost:8000`

### 4. Configurar Frontend
```bash
# Instalar dependencias Node.js
cd frontend
npm install

# Ejecutar servidor de desarrollo
npm run dev
```

El frontend estará disponible en `http://localhost:3000`

## 🎯 Uso

1. **Página de inicio**: Interfaz de bienvenida con información del proyecto
2. **Explorar noticias**: Acceder a la página principal de noticias
3. **Filtrar contenido**: Seleccionar entre IA, Marketing o ambos
4. **Refrescar**: Obtener las últimas noticias
5. **Leer más**: Enlaces directos a los artículos originales
6. **Cambiar tema**: Toggle entre modo claro y oscuro

## 🔧 API Endpoints

### `GET /api/get-news`
Obtiene noticias filtradas según el parámetro especificado.

**Parámetros:**
- `filter_type` (string): 'ai', 'marketing', 'both'

**Respuesta:**
```json
{
  "status": "success",
  "filter": "both",
  "count": 10,
  "news": [
    {
      "title": "AI is revolutionizing marketing",
      "description": "Summary here",
      "url": "https://...",
      "image": "https://...",
      "publishedAt": "2024-08-08T10:00:00Z",
      "source": "Tech News",
      "category": "both"
    }
  ]
}
```

### `GET /health`
Verificación de estado del servidor.

## 🤖 Agente LangGraph

El agente utiliza un pipeline de tres etapas:

1. **Fetch News**: Consulta NewsAPI con query optimizada
2. **Filter News**: Filtra noticias relevantes por palabras clave
3. **Summarize**: Resume descripciones largas usando OpenAI

## 🎨 Componentes UI

La interfaz está construida con componentes reutilizables:

- `Button` - Botones con variantes y tamaños
- `Card` - Tarjetas para mostrar contenido
- `Select` - Selectores de filtros
- `Badge` - Etiquetas de categorías
- `ThemeProvider` - Contexto para manejo de temas

## 📱 Responsive Design

La aplicación está optimizada para:
- 📱 Móviles (320px+)
- 📋 Tablets (768px+)
- 🖥️ Desktop (1024px+)

## 🌙 Modo Oscuro

Soporte completo para tema oscuro con:
- Persistencia en localStorage
- Transiciones suaves
- Colores optimizados para legibilidad

## 🚀 Despliegue

### HuggingFace Spaces (Recomendado)

1. Crear nuevo Space en HuggingFace
2. Seleccionar "Gradio" como framework
3. Subir código y configurar variables de entorno
4. La aplicación se desplegará automáticamente

### Docker (Alternativo)

```dockerfile
# Dockerfile ejemplo para el backend
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .
CMD ["python", "main.py"]
```

## 🧪 Testing

### Backend
```bash
cd backend
python agent/langgraph_agent.py  # Test del agente
```

### Frontend
```bash
cd frontend
npm run build  # Verificar build
```

## 📊 Monitoreo

- Logs del backend en consola
- Métricas de respuesta de APIs
- Estados de error manejados en frontend

## 🔒 Seguridad

- Variables de entorno para claves sensibles
- Validación de inputs en backend
- CORS configurado para desarrollo
- Rate limiting (recomendado para producción)

## 🤝 Contribución

Este es un proyecto de prueba técnica. Para mejoras:

1. Fork del repositorio
2. Crear feature branch
3. Commit de cambios
4. Push y crear Pull Request

## 📝 Licencia

Proyecto de prueba técnica para Dentsu.

## 📞 Contacto

Para dudas sobre la implementación o el proyecto, contactar al desarrollador.

---

**Desarrollado con ❤️ para Dentsu - Prueba Técnica 2024**
AI &amp; Marketing news agentic searcher web - Technical Challenge - Dentsu
