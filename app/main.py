"""
Aplicação principal da GitHub Data API
"""

import time
import uuid
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.routes import router
from app.utils.logger import logger, log_request, setup_logging

# Configuração de logging
setup_logging()

# Criação da aplicação FastAPI
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="""
# 🚀 GitHub Data API

Uma API completa para buscar dados do GitHub de forma eficiente e organizada.

## ✨ Funcionalidades

- **👤 Usuários**: Dados de perfil, repositórios, linguagens e estatísticas
- **📦 Repositórios**: Informações detalhadas, commits, issues e pull requests
- **🔍 Busca**: Repositórios e usuários com filtros avançados
- **🧠 Cache**: Sistema de cache inteligente para melhor performance
- **📊 Monitoramento**: Logs estruturados e métricas de performance

## 🛠️ Tecnologias

- **FastAPI**: Framework web moderno e rápido
- **Pydantic**: Validação de dados e serialização
- **httpx**: Cliente HTTP assíncrono
- **Redis**: Cache distribuído (opcional)
- **Docker**: Containerização completa

## 📚 Documentação

- **Swagger UI**: `/docs` - Interface interativa
- **ReDoc**: `/redoc` - Documentação alternativa
- **OpenAPI**: `/openapi.json` - Especificação JSON

## 🚀 Deploy

- **Render.com**: Deploy automático
- **Docker**: Containerização
- **Health Check**: `/api/v1/health`

---
**Desenvolvido com ❤️ para facilitar o acesso aos dados do GitHub**
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "GitHub Data API",
        "url": "https://github.com/seu-usuario/git-api",
        "email": "seu-email@exemplo.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    servers=[
        {"url": "http://localhost:8000", "description": "Desenvolvimento local"},
        {"url": "https://github-data-api.onrender.com", "description": "Produção (Render.com)"},
    ]
)

# Middleware de logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware para logar todas as requisições"""
    request_id = str(uuid.uuid4())
    start_time = time.time()
    
    # Log da requisição
    logger.info(f"Request {request_id}: {request.method} {request.url}")
    
    # Processa a requisição
    response = await call_next(request)
    
    # Calcula duração
    duration = time.time() - start_time
    
    # Log da resposta
    log_request(
        request_id=request_id,
        method=request.method,
        url=str(request.url),
        status_code=response.status_code,
        duration=duration
    )
    
    # Adiciona headers de performance
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Response-Time"] = str(duration)
    
    return response

# Configuração de CORS
def get_cors_origins():
    """Retorna as origens permitidas para CORS"""
    if settings.debug:
        # Em desenvolvimento, permite todas as origens
        return ["*"]
    else:
        # Em produção, permite apenas origens específicas
        origins = [
            "https://github-data-api.onrender.com",
            "https://github.com",
            "https://gist.github.com",
            "https://raw.githubusercontent.com",
            "http://localhost:3000",  # Para desenvolvimento frontend
            "http://localhost:8080",  # Para desenvolvimento frontend
        ]
        # Adiciona origens customizadas se configuradas
        if hasattr(settings, 'cors_origins') and settings.cors_origins:
            origins.extend(settings.cors_origins)
        return origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=[
        "Accept",
        "Accept-Language",
        "Content-Language",
        "Content-Type",
        "Authorization",
        "X-Requested-With",
        "X-API-Key",
        "X-Request-ID",
    ],
    expose_headers=[
        "X-Request-ID",
        "X-Response-Time",
        "X-Cache-Hit",
        "X-Rate-Limit-Remaining",
    ],
    max_age=86400,  # Cache preflight por 24 horas
)

# Inclusão das rotas
app.include_router(router)

# Rota raiz
@app.get("/", summary="Página inicial")
async def root():
    """
    Página inicial da API.
    
    Returns:
        Informações sobre a API
    """
    return {
        "message": "Bem-vindo à GitHub Data API",
        "version": settings.api_version,
        "description": settings.api_description,
        "docs": "/docs",
        "health": "/api/v1/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    ) 