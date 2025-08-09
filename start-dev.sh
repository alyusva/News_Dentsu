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

# Instalar dependencias backend
echo "📦 Instalando dependencias del backend..."
pip3 install -r requirements.txt

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
cd backend && python3 main_local.py &
BACKEND_PID=$!
cd ..

# Esperar a que el backend inicie
sleep 3

# Iniciar frontend
echo "⚡ Iniciando frontend en puerto 3000..."
cd frontend && npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Servicios iniciados:"
echo "   🔗 Backend:  http://localhost:8000"
echo "   🔗 Frontend: http://localhost:3000"
echo "   � API Docs: http://localhost:8000/docs"
echo ""
echo "🛑 Para detener: Ctrl+C"

# Función para limpiar procesos al salir
cleanup() {
    echo ""
    echo "🛑 Deteniendo servicios..."
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    exit 0
}

trap cleanup SIGINT SIGTERM

# Mantener el script corriendo
wait
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
# Activar entorno virtual si existe
if [ -d "venv" ]; then
    source venv/bin/activate
fi
cd backend
python3 main_local.py &
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
