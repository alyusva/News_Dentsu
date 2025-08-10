#!/bin/bash

# 🚀 Plataforma de Noticias IA y Marketing - Dentsu
echo "🚀 Iniciando desarrollo local..."

# Verificar .env
if [ ! -f ".env" ]; then
    echo "❌ Archivo .env no encontrado. Copiando desde .env.example"
    cp .env.example .env
    echo "⚠️  Configura tus API keys en .env antes de continuar"
    exit 1
fi

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "🔧 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "📦 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias backend
echo "📦 Instalando dependencias del backend..."
pip install -r requirements.txt

# Instalar dependencias frontend
echo "📦 Instalando dependencias del frontend..."
cd frontend && npm install && cd ..

# Verificar puertos
if lsof -ti:8000 > /dev/null; then
    echo "⚠️  Puerto 8000 ocupado. Deteniendo proceso..."
    kill $(lsof -ti:8000) 2>/dev/null || true
fi

if lsof -ti:3000 > /dev/null; then
    echo "⚠️  Puerto 3000 ocupado. Deteniendo proceso..."
    kill $(lsof -ti:3000) 2>/dev/null || true
fi

echo "🔥 Iniciando servicios..."

# Iniciar backend
echo "🐍 Iniciando backend en puerto 8000..."
(cd backend && python main.py) &
BACKEND_PID=$!

# Esperar a que el backend inicie
sleep 3

# Iniciar frontend
echo "⚛️  Iniciando frontend en puerto 3000..."
(cd frontend && npm run dev) &
FRONTEND_PID=$!

# Esperar a que el frontend inicie
sleep 2

echo ""
echo "✅ Servicios iniciados:"
echo "   🔗 Frontend: http://localhost:3000"
echo "   🔗 Backend:  http://localhost:8000"
echo "   📖 API Docs: http://localhost:8000/docs"
echo ""
echo "🛑 Para detener: Ctrl+C"

# Función para limpiar procesos al salir
cleanup() {
    echo ""
    echo "🛑 Deteniendo servicios..."
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    deactivate 2>/dev/null || true
    exit 0
}

trap cleanup SIGINT SIGTERM

# Mantener el script corriendo
wait
