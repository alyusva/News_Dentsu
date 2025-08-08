import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Select } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { useTheme } from '@/components/ThemeProvider';
import { 
  ArrowLeft, 
  RefreshCw, 
  Sun, 
  Moon, 
  Sparkles, 
  ExternalLink,
  Brain,
  TrendingUp,
  Calendar,
  Loader2
} from 'lucide-react';

const NewsPage = () => {
  const navigate = useNavigate();
  const { theme, toggleTheme } = useTheme();
  
  // Estados
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState(() => {
    // Obtener filtro guardado del localStorage
    return localStorage.getItem('newsFilter') || 'both';
  });
  const [error, setError] = useState(null);

  // Función para obtener noticias del backend
  const fetchNews = async (filterType = filter) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`/api/get-news?filter_type=${filterType}`);
      
      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      
      if (data.status === 'success') {
        setNews(data.news || []);
      } else {
        throw new Error('Error en la respuesta del servidor');
      }
    } catch (err) {
      console.error('Error al obtener noticias:', err);
      setError(err.message);
      
      // Mostrar datos de ejemplo en caso de error para demostración
      setNews(getSampleNews());
    } finally {
      setLoading(false);
    }
  };

  // Datos de ejemplo para demostración
  const getSampleNews = () => [
    {
      title: "AI Revolutionizes Digital Marketing Strategies",
      description: "New artificial intelligence tools are transforming how marketers reach and engage with their audiences.",
      url: "https://example.com/ai-marketing-1",
      image: "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=400&h=250&fit=crop",
      publishedAt: "2024-08-08T10:00:00Z",
      source: "Tech News",
      category: "both"
    },
    {
      title: "Machine Learning Enhances Customer Segmentation",
      description: "Advanced ML algorithms are helping businesses better understand and categorize their customer base.",
      url: "https://example.com/ml-segmentation",
      image: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&h=250&fit=crop",
      publishedAt: "2024-08-08T09:30:00Z",
      source: "Marketing Today",
      category: "both"
    },
    {
      title: "ChatGPT Integration in Marketing Automation",
      description: "Companies are integrating generative AI into their marketing workflows for improved efficiency.",
      url: "https://example.com/chatgpt-marketing",
      image: "https://images.unsplash.com/photo-1676299081847-824916de030a?w=400&h=250&fit=crop",
      publishedAt: "2024-08-08T08:45:00Z",
      source: "AI Weekly",
      category: "ai"
    }
  ];

  // Efecto para cargar noticias al montar el componente
  useEffect(() => {
    fetchNews();
  }, []);

  // Manejar cambio de filtro
  const handleFilterChange = (newFilter) => {
    setFilter(newFilter);
    localStorage.setItem('newsFilter', newFilter);
    fetchNews(newFilter);
  };

  // Manejar refresh de noticias
  const handleRefresh = () => {
    fetchNews();
  };

  // Obtener icono según categoría
  const getCategoryIcon = (category) => {
    switch (category) {
      case 'ai':
        return <Brain className="w-4 h-4" />;
      case 'marketing':
        return <TrendingUp className="w-4 h-4" />;
      case 'both':
        return <Sparkles className="w-4 h-4" />;
      default:
        return <Sparkles className="w-4 h-4" />;
    }
  };

  // Obtener color de badge según categoría
  const getCategoryColor = (category) => {
    switch (category) {
      case 'ai':
        return 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300';
      case 'marketing':
        return 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300';
      case 'both':
        return 'bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-300';
      default:
        return 'bg-gray-100 text-gray-700 dark:bg-gray-900/30 dark:text-gray-300';
    }
  };

  // Formatear fecha
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
      day: '2-digit',
      month: 'short',
      year: 'numeric'
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 dark:from-slate-900 dark:to-slate-800">
      {/* Header */}
      <header className="bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm border-b border-gray-200 dark:border-slate-700 sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => navigate('/')}
                className="flex items-center space-x-2"
              >
                <ArrowLeft className="w-4 h-4" />
                <span>Volver</span>
              </Button>
              
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                  <Sparkles className="w-5 h-5 text-white" />
                </div>
                <h1 className="text-xl font-bold text-gray-900 dark:text-white">
                  Noticias IA & Marketing
                </h1>
              </div>
            </div>
            
            <div className="flex items-center space-x-3">
              {/* Filtro */}
              <Select
                value={filter}
                onChange={(e) => handleFilterChange(e.target.value)}
                className="w-40"
              >
                <option value="both">Ambos</option>
                <option value="ai">Solo IA</option>
                <option value="marketing">Solo Marketing</option>
              </Select>
              
              {/* Botón Refresh */}
              <Button
                variant="outline"
                size="sm"
                onClick={handleRefresh}
                disabled={loading}
                className="flex items-center space-x-2"
              >
                <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
                <span>Refrescar</span>
              </Button>
              
              {/* Toggle tema */}
              <Button
                variant="ghost"
                size="icon"
                onClick={toggleTheme}
                className="rounded-full"
              >
                {theme === 'light' ? (
                  <Moon className="h-5 w-5" />
                ) : (
                  <Sun className="h-5 w-5" />
                )}
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {/* Estado de carga */}
        {loading && (
          <div className="flex items-center justify-center py-16">
            <div className="text-center">
              <Loader2 className="w-8 h-8 animate-spin mx-auto mb-4 text-blue-600" />
              <p className="text-gray-600 dark:text-gray-400">Cargando noticias...</p>
            </div>
          </div>
        )}

        {/* Error */}
        {error && !loading && (
          <div className="max-w-md mx-auto mb-8">
            <Card className="border-red-200 bg-red-50 dark:bg-red-900/20 dark:border-red-800">
              <CardContent className="p-4">
                <p className="text-red-600 dark:text-red-400 text-center">
                  Error al cargar noticias: {error}
                </p>
                <p className="text-sm text-red-500 dark:text-red-300 text-center mt-2">
                  Mostrando datos de ejemplo
                </p>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Grid de noticias */}
        {!loading && news.length > 0 && (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {news.map((article, index) => (
              <Card 
                key={index} 
                className="news-card-hover overflow-hidden border-0 shadow-lg hover:shadow-xl transition-all duration-300"
              >
                {/* Imagen */}
                <div className="relative h-48 overflow-hidden">
                  <img
                    src={article.image || 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=400&h=250&fit=crop'}
                    alt={article.title}
                    className="w-full h-full object-cover transition-transform duration-300 hover:scale-105"
                    onError={(e) => {
                      e.target.src = 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=400&h=250&fit=crop';
                    }}
                  />
                  
                  {/* Badge de categoría */}
                  <div className="absolute top-3 left-3">
                    <Badge className={`${getCategoryColor(article.category)} border-0 flex items-center space-x-1`}>
                      {getCategoryIcon(article.category)}
                      <span className="capitalize">
                        {article.category === 'both' ? 'IA + Marketing' : 
                         article.category === 'ai' ? 'IA' : 'Marketing'}
                      </span>
                    </Badge>
                  </div>
                </div>

                <CardHeader className="pb-3">
                  <div className="flex items-center space-x-2 text-sm text-gray-500 dark:text-gray-400 mb-2">
                    <Calendar className="w-4 h-4" />
                    <span>{formatDate(article.publishedAt)}</span>
                    {article.source && (
                      <>
                        <span>•</span>
                        <span>{article.source}</span>
                      </>
                    )}
                  </div>
                  
                  <CardTitle className="text-lg leading-tight line-clamp-2">
                    {article.title}
                  </CardTitle>
                </CardHeader>

                <CardContent className="pt-0">
                  <CardDescription className="line-clamp-3 mb-4">
                    {article.description}
                  </CardDescription>

                  <Button
                    asChild
                    variant="outline"
                    size="sm"
                    className="w-full group"
                  >
                    <a
                      href={article.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center justify-center space-x-2"
                    >
                      <span>Leer más</span>
                      <ExternalLink className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                    </a>
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {/* Estado vacío */}
        {!loading && news.length === 0 && !error && (
          <div className="text-center py-16">
            <div className="w-16 h-16 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center mx-auto mb-4">
              <Sparkles className="w-8 h-8 text-gray-400" />
            </div>
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
              No se encontraron noticias
            </h3>
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              Intenta cambiar el filtro o actualizar las noticias
            </p>
            <Button onClick={handleRefresh} variant="outline">
              Refrescar noticias
            </Button>
          </div>
        )}
      </main>
    </div>
  );
};

export default NewsPage;
