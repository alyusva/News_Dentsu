#!/bin/bash

# Script de preparación del entorno
# Plataforma de Noticias IA y Marketing - Dentsu
# Este script instala todas las dependencias y verifica que todo funcione correctamente

set -e  # Salir si cualquier comando falla

echo "🚀 Preparando entorno para Plataforma de Noticias IA y Marketing"
echo "================================================================="
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir con colores
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Función para verificar si un comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Función para verificar version de Python
check_python_version() {
    if command_exists python3; then
        local python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        local required_version="3.9"
        
        if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
            print_status "Python $python_version detectado (✓ >= 3.9)"
            return 0
        else
            print_error "Python $python_version es muy antiguo. Se requiere >= 3.9"
            return 1
        fi
    else
        print_error "Python 3 no está instalado"
        return 1
    fi
}

# Función para verificar version de Node.js
check_node_version() {
    if command_exists node; then
        local node_version=$(node -v | sed 's/v//')
        local required_version="18.0.0"
        
        if [ "$(printf '%s\n' "$required_version" "$node_version" | sort -V | head -n1)" = "$required_version" ]; then
            print_status "Node.js $node_version detectado (✓ >= 18.0.0)"
            return 0
        else
            print_error "Node.js $node_version es muy antiguo. Se requiere >= 18.0.0"
            return 1
        fi
    else
        print_error "Node.js no está instalado"
        return 1
    fi
}

# Función para verificar archivo .env
check_env_file() {
    if [ -f ".env" ]; then
        print_status "Archivo .env encontrado"
        
        # Verificar que las claves principales estén configuradas
        if grep -q "OPENAI_API_KEY=sk-" .env && grep -q "NEWS_API_KEY=" .env; then
            print_status "API Keys configuradas correctamente"
            return 0
        else
            print_warning "API Keys no están configuradas correctamente en .env"
            print_info "Asegúrate de tener:"
            echo "  - OPENAI_API_KEY=sk-..."
            echo "  - NEWS_API_KEY=..."
            return 1
        fi
    else
        print_warning "Archivo .env no encontrado"
        print_info "Copiando .env.example a .env..."
        cp .env.example .env
        print_error "Por favor configura tus API keys en .env antes de continuar"
        return 1
    fi
}

# Función para verificar dependencias del sistema
check_system_dependencies() {
    print_info "Verificando dependencias del sistema..."
    
    local all_good=true
    
    # Verificar Python
    if ! check_python_version; then
        all_good=false
    fi
    
    # Verificar Node.js
    if ! check_node_version; then
        all_good=false
    fi
    
    # Verificar npm
    if command_exists npm; then
        print_status "npm $(npm -v) detectado"
    else
        print_error "npm no está instalado"
        all_good=false
    fi
    
    # Verificar pip
    if command_exists pip3; then
        print_status "pip3 detectado"
    elif command_exists pip; then
        print_status "pip detectado"
    else
        print_error "pip no está instalado"
        all_good=false
    fi
    
    # Verificar git
    if command_exists git; then
        print_status "git $(git --version | cut -d' ' -f3) detectado"
    else
        print_error "git no está instalado"
        all_good=false
    fi
    
    if [ "$all_good" = false ]; then
        print_error "Faltan dependencias del sistema. Por favor instálalas antes de continuar."
        return 1
    fi
    
    print_status "Todas las dependencias del sistema están disponibles"
    return 0
}

# Función para instalar dependencias de Python
install_python_dependencies() {
    print_info "Instalando dependencias de Python..."
    
    # Crear entorno virtual si no existe
    if [ ! -d "venv" ]; then
        print_info "Creando entorno virtual..."
        python3 -m venv venv
    fi
    
    # Activar entorno virtual
    print_info "Activando entorno virtual..."
    source venv/bin/activate
    
    # Actualizar pip
    print_info "Actualizando pip..."
    pip install --upgrade pip
    
    # Instalar dependencias
    print_info "Instalando paquetes desde requirements.txt..."
    pip install -r requirements.txt
    
    print_status "Dependencias de Python instaladas correctamente"
    
    # Verificar instalación
    print_info "Verificando instalación de paquetes clave..."
    python -c "import fastapi; print(f'FastAPI {fastapi.__version__}')" && print_status "FastAPI OK"
    python -c "import openai; print(f'OpenAI {openai.__version__}')" && print_status "OpenAI OK"
    python -c "import requests; print(f'Requests {requests.__version__}')" && print_status "Requests OK"
    
    # Intentar importar langgraph (puede fallar, es normal)
    if python -c "import langgraph" 2>/dev/null; then
        print_status "LangGraph OK"
    else
        print_warning "LangGraph no se pudo importar (puede ser normal si la versión no está disponible)"
    fi
    
    deactivate
}

# Función para instalar dependencias de Node.js
install_node_dependencies() {
    print_info "Instalando dependencias de Node.js para el frontend..."
    
    cd frontend
    
    # Limpiar cache npm si existe
    if [ -d "node_modules" ]; then
        print_info "Limpiando instalación anterior..."
        rm -rf node_modules package-lock.json
    fi
    
    # Instalar dependencias
    print_info "Ejecutando npm install..."
    npm install
    
    print_status "Dependencias de Node.js instaladas correctamente"
    
    # Verificar que los paquetes principales estén instalados
    if [ -d "node_modules/react" ]; then
        print_status "React instalado"
    fi
    
    if [ -d "node_modules/vite" ]; then
        print_status "Vite instalado"
    fi
    
    if [ -d "node_modules/tailwindcss" ]; then
        print_status "Tailwind CSS instalado"
    fi
    
    cd ..
}

# Función para verificar que los servicios funcionen
test_services() {
    print_info "Probando servicios..."
    
    # Activar entorno virtual
    source venv/bin/activate
    
    # Probar que el backend puede iniciarse
    print_info "Verificando que el backend puede iniciarse..."
    cd backend
    
    # Probar importaciones del backend
    if python -c "from main import app; print('Backend imports OK')" 2>/dev/null; then
        print_status "Backend puede importarse correctamente"
    else
        print_error "Error al importar el backend"
        cd ..
        deactivate
        return 1
    fi
    
    cd ..
    
    # Probar que el frontend puede construirse
    print_info "Verificando que el frontend puede construirse..."
    cd frontend
    
    if npm run build >/dev/null 2>&1; then
        print_status "Frontend puede construirse correctamente"
        # Limpiar build de prueba
        rm -rf dist
    else
        print_error "Error al construir el frontend"
        cd ..
        deactivate
        return 1
    fi
    
    cd ..
    deactivate
    
    print_status "Todos los servicios pueden ejecutarse correctamente"
}

# Función para mostrar instrucciones finales
show_final_instructions() {
    echo ""
    echo "🎉 ¡Entorno preparado exitosamente!"
    echo "=================================="
    echo ""
    print_info "Para ejecutar la aplicación:"
    echo "  1. Asegúrate de que tus API keys estén configuradas en .env"
    echo "  2. Ejecuta: ./start-dev.sh"
    echo ""
    print_info "URLs de acceso:"
    echo "  - Frontend: http://localhost:3000"
    echo "  - Backend:  http://localhost:8000"
    echo "  - API Docs: http://localhost:8000/docs"
    echo ""
    print_info "Para HuggingFace Spaces:"
    echo "  - Ejecuta: python app.py"
    echo "  - Accede: http://localhost:7860"
    echo ""
    print_status "¡Todo listo para la demostración!"
}

# Función principal
main() {
    echo "🔍 Iniciando verificación del entorno..."
    echo ""
    
    # Verificar dependencias del sistema
    if ! check_system_dependencies; then
        exit 1
    fi
    
    echo ""
    print_info "✅ Verificaciones del sistema completadas"
    echo ""
    
    # Verificar archivo .env
    if ! check_env_file; then
        print_error "Configura el archivo .env antes de continuar"
        exit 1
    fi
    
    echo ""
    
    # Instalar dependencias de Python
    install_python_dependencies
    echo ""
    
    # Instalar dependencias de Node.js
    install_node_dependencies
    echo ""
    
    # Probar servicios
    test_services
    echo ""
    
    # Mostrar instrucciones finales
    show_final_instructions
}

# Verificar que estamos en el directorio correcto
if [ ! -f "requirements.txt" ] || [ ! -d "frontend" ] || [ ! -d "backend" ]; then
    print_error "Este script debe ejecutarse desde el directorio raíz del proyecto"
    print_info "Asegúrate de estar en el directorio que contiene requirements.txt, frontend/ y backend/"
    exit 1
fi

# Ejecutar función principal
main "$@"
