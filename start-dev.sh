#!/bin/bash

# Script de inicio para el desarrollo local
# Plataforma de Noticias IA y Marketing - Dentsu

echo "🚀 Iniciando Plataforma de Noticias IA y Marketing"
echo "=================================================="

# Verificar si existe el archivo .env
if [ ! -f ".env" ]; then
    echo "❌ Archivo .env no encontrado"
    echo "📋 Copiando .env.example a .env..."
    cp .env.example .env
    echo "⚠️  Por favor configura tus API keys en el archivo .env"
    echo "   - OPENAI_API_KEY=tu_openai_api_key"
    echo "   - NEWS_API_KEY=tu_news_api_key"
    exit 1
fi

# Función para verificar si un puerto está ocupado
check_port() {
    lsof -ti:$1 > /dev/null
    return $?
}

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado"
    exit 1
fi

# Verificar Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js no está instalado"
    exit 1
fi

echo "✅ Verificaciones pasadas"

# Instalar dependencias del backend si no existen
if [ ! -d "backend/__pycache__" ]; then
    echo "📦 Instalando dependencias del backend..."
    pip3 install -r requirements.txt
fi

# Instalar dependencias del frontend si no existen
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Instalando dependencias del frontend..."
    cd frontend
    npm install
    cd ..
fi

echo "🔥 Iniciando servidores..."

# Verificar puertos
if check_port 8000; then
    echo "⚠️  Puerto 8000 ocupado (Backend)"
    read -p "¿Quieres matar el proceso? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        lsof -ti:8000 | xargs kill -9
    else
        echo "❌ Cancelando inicio"
        exit 1
    fi
fi

if check_port 3000; then
    echo "⚠️  Puerto 3000 ocupado (Frontend)"
    read -p "¿Quieres matar el proceso? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        lsof -ti:3000 | xargs kill -9
    else
        echo "❌ Cancelando inicio"
        exit 1
    fi
fi

# Iniciar backend en background
echo "🐍 Iniciando backend en puerto 8000..."
cd backend
python3 main.py &
BACKEND_PID=$!
cd ..

# Esperar a que el backend esté listo
sleep 3

# Iniciar frontend en background
echo "⚛️  Iniciando frontend en puerto 3000..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "🎉 ¡Aplicación iniciada exitosamente!"
echo "=================================================="
echo "🌐 Frontend: http://localhost:3000"
echo "🔌 Backend:  http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Para detener la aplicación, presiona Ctrl+C"

# Función para limpiar procesos al salir
cleanup() {
    echo ""
    echo "🛑 Deteniendo servidores..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Aplicación detenida"
    exit 0
}

# Capturar Ctrl+C
trap cleanup SIGINT

# Esperar indefinidamente
wait
