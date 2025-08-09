# 📰 Plataforma de Noticias IA y Marketing - Dentsu

Plataforma inteligente de agregación de noticias desarrollada para la entrevista técnica de Dentsu. Combina **FastAPI + LangGraph + React** para crear una experiencia de noticias potenciada por IA.

## 🚀 Características

### Backend (FastAPI + LangGraph)
- **🤖 Agente LangGraph** con 10 nodos especializados
- **📡 Integración NewsAPI** para noticias en tiempo real
- **🧠 OpenAI GPT** para análisis inteligente
- **🏷️ Categorización automática** (IA vs Marketing)
- **🔍 Filtrado inteligente** y deduplicación
- **📊 API REST** completamente documentada

### Frontend (React + Tailwind CSS)
- **⚛️ React 18** con hooks modernos
- **🎨 Tailwind CSS** para diseño responsivo
- **🌐 React Router** para navegación fluida
- **📱 Diseño responsive** profesional
- **🔄 Estados de carga** y manejo de errores

## 🏗️ Arquitectura

```
News_Dentsu/
├── backend/                 # API FastAPI + LangGraph
│   ├── app/
│   │   ├── agent/          # LangGraph Agent (10 nodos)
│   │   ├── api/            # Endpoints REST
│   │   └── core/           # Configuración
│   └── main_local.py       # Servidor desarrollo
├── frontend/               # React + Tailwind
│   └── src/
│       ├── components/     # Componentes UI
│       └── pages/          # Páginas principales
└── scripts/                # Scripts automatización
```

## ⚡ Inicio Rápido

### 1. Clonar y configurar
```bash
git clone https://github.com/alyusva/News_Dentsu.git
cd News_Dentsu

# Hacer ejecutable el script
chmod +x start-dev.sh
```

### 2. Configurar API Keys
```bash
# Editar .env con tus keys
cp .env.example .env
# Añadir tus API keys:
# OPENAI_API_KEY=sk-...
# NEWS_API_KEY=...
```

### 3. Ejecutar aplicación
```bash
# Iniciar frontend + backend
./start-dev.sh
```

### 4. Acceder a la aplicación
- **🌐 Frontend**: http://localhost:3000
- **🔌 Backend**: http://localhost:8000  
- **📚 API Docs**: http://localhost:8000/docs

## 🔧 Desarrollo

### Backend independiente
```bash
cd backend
source ../venv/bin/activate
python main_local.py
```

### Frontend independiente
```bash
cd frontend
npm install
npm run dev
```

## 🎯 Para Dentsu

### Demostración técnica
1. **Arquitectura moderna**: Microservicios + IA
2. **LangGraph Agent**: Procesamiento inteligente de noticias
3. **UI/UX profesional**: React + Tailwind CSS
4. **APIs documentadas**: Swagger/OpenAPI
5. **Código limpio**: Estructura profesional

### Casos de uso
- 📊 **Dashboard ejecutivo** con noticias relevantes
- 🎯 **Análisis de mercado** automatizado  
- 📈 **Tendencias IA/Marketing** en tiempo real
- 🔍 **Búsqueda inteligente** de contenido

## 🌐 Despliegue Producción

- **Backend**: Google Cloud Run (desplegado)
- **Frontend**: Vercel (desplegado)
- **URL Producción**: https://news-dentsu-frontend.vercel.app

## 🛠️ Stack Tecnológico

**Backend**
- FastAPI 0.111.0
- LangGraph 0.6.4
- OpenAI 1.99.5
- NewsAPI
- Python 3.11+

**Frontend**
- React 18.2.0
- Vite 5.2.0
- Tailwind CSS 3.4.4
- Lucide React (iconos)

## 📋 Scripts Disponibles

- `./setup-environment.sh` - Configuración completa del entorno
- `./start-dev.sh` - Inicio de desarrollo (frontend + backend)
- `./deploy-cloudrun.sh` - Despliegue a Google Cloud Run

## 🎉 Estado del Proyecto

✅ **Backend**: Funcionando con LangGraph + NewsAPI  
✅ **Frontend**: Interface React completa  
✅ **Integración**: API endpoints conectados  
✅ **Despliegue**: Producción en Google Cloud Run  
✅ **Documentación**: API docs auto-generadas  

---

**Desarrollado para Dentsu** - Demostrando expertise en arquitecturas modernas, IA y desarrollo full-stack.
