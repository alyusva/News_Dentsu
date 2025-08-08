import React from 'react';
import { Github, Linkedin, Mail, ExternalLink } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="bg-gray-900 dark:bg-gray-950 text-white py-12 mt-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Información del proyecto */}
          <div className="space-y-4">
            <h3 className="text-xl font-bold text-blue-400">
              Plataforma de Noticias IA y Marketing
            </h3>
            <p className="text-gray-400 text-sm">
              Sistema inteligente de agregación de noticias desarrollado con FastAPI, 
              LangGraph y React. Utiliza IA para filtrar y resumir contenido relevante 
              sobre Inteligencia Artificial y Marketing.
            </p>
            <div className="flex flex-wrap gap-2">
              <span className="px-2 py-1 bg-blue-600 text-xs rounded">FastAPI</span>
              <span className="px-2 py-1 bg-green-600 text-xs rounded">LangGraph</span>
              <span className="px-2 py-1 bg-purple-600 text-xs rounded">OpenAI</span>
              <span className="px-2 py-1 bg-cyan-600 text-xs rounded">React</span>
            </div>
          </div>

          {/* Información del desarrollador */}
          <div className="space-y-4">
            <h3 className="text-xl font-bold text-blue-400">Desarrollado por</h3>
            <div className="space-y-2">
              <h4 className="text-lg font-semibold">Álvaro Yuste Valles</h4>
              <p className="text-gray-400 text-sm">
                Process Engineer & AI/ML Developer
              </p>
              <p className="text-gray-400 text-sm">
                Especialista en automatización industrial, inteligencia artificial 
                y análisis de datos. Actualmente en Signify (Philips Lighting).
              </p>
            </div>
          </div>

          {/* Enlaces y contacto */}
          <div className="space-y-4">
            <h3 className="text-xl font-bold text-blue-400">Conecta conmigo</h3>
            <div className="space-y-3">
              <a 
                href="https://www.linkedin.com/in/alvaro-yuste-valles" 
                target="_blank" 
                rel="noopener noreferrer"
                className="flex items-center space-x-2 text-gray-400 hover:text-blue-400 transition-colors duration-200"
              >
                <Linkedin size={18} />
                <span>LinkedIn</span>
                <ExternalLink size={14} />
              </a>
              
              <a 
                href="https://github.com/alyusva" 
                target="_blank" 
                rel="noopener noreferrer"
                className="flex items-center space-x-2 text-gray-400 hover:text-blue-400 transition-colors duration-200"
              >
                <Github size={18} />
                <span>GitHub</span>
                <ExternalLink size={14} />
              </a>
              
              <a 
                href="https://www.alvaro-yuste.com" 
                target="_blank" 
                rel="noopener noreferrer"
                className="flex items-center space-x-2 text-gray-400 hover:text-blue-400 transition-colors duration-200"
              >
                <ExternalLink size={18} />
                <span>Portfolio</span>
                <ExternalLink size={14} />
              </a>
              
              <a 
                href="mailto:alyusva@gmail.com"
                className="flex items-center space-x-2 text-gray-400 hover:text-blue-400 transition-colors duration-200"
              >
                <Mail size={18} />
                <span>Email</span>
              </a>
            </div>
          </div>
        </div>

        {/* Línea separadora y copyright */}
        <div className="border-t border-gray-800 mt-8 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
            <p className="text-gray-400 text-sm">
              © 2025 Álvaro Yuste Valles. Desarrollado para entrevista técnica Dentsu.
            </p>
            <div className="flex items-center space-x-4 text-xs text-gray-500">
              <span>Proyecto Open Source</span>
              <span>•</span>
              <span>Agosto 2025</span>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
