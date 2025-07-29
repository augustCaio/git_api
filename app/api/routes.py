"""
Endpoints da API para dados do GitHub
"""

from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, HTTPException, Query, Depends
from app.services.github_client import GitHubClient
from app.models.github_models import (
    GitHubUser,
    GitHubRepository,
    GitHubLanguage,
    GitHubEvent,
    GitHubCommit,
    GitHubIssue,
    GitHubPullRequest,
)
from app.config import settings

router = APIRouter(prefix="/api/v1", tags=["GitHub Data"])


async def get_github_client() -> GitHubClient:
    """Dependency para obter o cliente do GitHub"""
    return GitHubClient()


@router.get("/users/{username}", response_model=GitHubUser, summary="Obter dados de usuário", tags=["Usuários"])
async def get_user(
    username: str,
    client: GitHubClient = Depends(get_github_client)
) -> GitHubUser:
    """
    ## 👤 Dados do Usuário
    
    Obtém informações completas de um usuário do GitHub.
    
    ### 📊 Dados Retornados
    
    - **Informações básicas**: ID, login, nome, email, bio
    - **Localização**: País, cidade, empresa
    - **Estatísticas**: Repositórios públicos, seguidores, seguindo
    - **Links**: Avatar, blog, site pessoal
    - **Status**: Tipo de conta, admin, verificado
    
    ### 🔄 Uso
    
    ```bash
    curl https://github-data-api.onrender.com/api/v1/users/octocat
    ```
    
    ### 📝 Exemplo de Resposta
    
    ```json
    {
      "id": 583231,
      "login": "octocat",
      "name": "The Octocat",
      "email": null,
      "avatar_url": "https://avatars.githubusercontent.com/u/583231?v=4",
      "bio": "GitHub mascot",
      "location": "San Francisco",
      "company": "@github",
      "public_repos": 10,
      "followers": 100,
      "following": 50
    }
    ```
    
    ### ⚠️ Limitações
    
    - Rate limit da API do GitHub: 60 requisições/hora (sem token)
    - Dados em cache por 5 minutos para melhor performance
    
    Args:
        username (str): Nome do usuário no GitHub

    Returns:
        GitHubUser: Dados completos do usuário
    """
    try:
        return await client.get_user(username)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Usuário {username} não encontrado: {str(e)}")


@router.get("/users/{username}/repositories", response_model=List[GitHubRepository], summary="Obter repositórios do usuário", tags=["Usuários"])
async def get_user_repositories(
    username: str,
    page: int = Query(1, ge=1, description="Número da página"),
    per_page: int = Query(30, ge=1, le=100, description="Itens por página"),
    client: GitHubClient = Depends(get_github_client)
) -> List[GitHubRepository]:
    """
    Obtém repositórios de um usuário do GitHub.
    
    Args:
        username: Nome do usuário no GitHub
        page: Número da página (padrão: 1)
        per_page: Itens por página (padrão: 30, máximo: 100)
        
    Returns:
        Lista de repositórios do usuário
    """
    try:
        return await client.get_user_repositories(username, page, per_page)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erro ao buscar repositórios: {str(e)}")


@router.get("/users/{username}/languages", summary="Obter linguagens do usuário", tags=["Usuários"])
async def get_user_languages(
    username: str,
    client: GitHubClient = Depends(get_github_client)
) -> dict:
    """
    Obtém as linguagens de programação mais usadas por um usuário.
    
    Args:
        username: Nome do usuário no GitHub
        
    Returns:
        Dicionário com linguagens e estatísticas
    """
    try:
        languages = await client.get_user_languages(username)
        return {
            "username": username,
            "languages": languages,
            "total_languages": len(languages)
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erro ao buscar linguagens: {str(e)}")


@router.get("/users/{username}/stats", summary="Obter estatísticas do usuário", tags=["Usuários"])
async def get_user_stats(
    username: str,
    client: GitHubClient = Depends(get_github_client)
) -> dict:
    """
    Obtém estatísticas detalhadas de um usuário do GitHub.
    
    Args:
        username: Nome do usuário no GitHub
        
    Returns:
        Estatísticas completas do usuário
    """
    try:
        stats = await client.get_user_stats(username)
        return {
            "username": username,
            "user": stats["user"],
            "repositories": stats["repositories"],
            "activity": stats["activity"],
            "languages": stats["languages"],
            "top_repositories": stats["top_repositories"]
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erro ao buscar estatísticas: {str(e)}")


@router.get("/repos/{owner}/{repo}", response_model=GitHubRepository, summary="Obter dados de repositório", tags=["Repositórios"])
async def get_repository(
    owner: str,
    repo: str,
    client: GitHubClient = Depends(get_github_client)
) -> GitHubRepository:
    """
    Obtém dados de um repositório específico.
    
    Args:
        owner: Proprietário do repositório
        repo: Nome do repositório
        
    Returns:
        Dados do repositório
    """
    try:
        return await client.get_repository(owner, repo)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Repositório {owner}/{repo} não encontrado: {str(e)}")


@router.get("/repos/{owner}/{repo}/languages", summary="Obter linguagens do repositório", tags=["Repositórios"])
async def get_repository_languages(
    owner: str,
    repo: str,
    client: GitHubClient = Depends(get_github_client)
) -> dict:
    """
    Obtém as linguagens de programação de um repositório.
    
    Args:
        owner: Proprietário do repositório
        repo: Nome do repositório
        
    Returns:
        Dicionário com linguagens e suas porcentagens
    """
    try:
        languages = await client.get_repository_languages(owner, repo)
        return {
            "repository": f"{owner}/{repo}",
            "languages": languages,
            "total_languages": len(languages)
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erro ao buscar linguagens: {str(e)}")


@router.get("/repos/{owner}/{repo}/events", response_model=List[GitHubEvent], summary="Obter eventos do repositório", tags=["Repositórios"])
async def get_repository_events(
    owner: str,
    repo: str,
    page: int = Query(1, ge=1, description="Número da página"),
    per_page: int = Query(30, ge=1, le=100, description="Itens por página"),
    client: GitHubClient = Depends(get_github_client)
) -> List[GitHubEvent]:
    """
    Obtém eventos de um repositório.
    
    Args:
        owner: Proprietário do repositório
        repo: Nome do repositório
        page: Número da página (padrão: 1)
        per_page: Itens por página (padrão: 30, máximo: 100)
        
    Returns:
        Lista de eventos do repositório
    """
    try:
        return await client.get_repository_events(owner, repo, page, per_page)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erro ao buscar eventos: {str(e)}")


@router.get("/repos/{owner}/{repo}/commits", response_model=List[GitHubCommit], summary="Obter commits do repositório", tags=["Repositórios"])
async def get_repository_commits(
    owner: str,
    repo: str,
    page: int = Query(1, ge=1, description="Número da página"),
    per_page: int = Query(30, ge=1, le=100, description="Itens por página"),
    client: GitHubClient = Depends(get_github_client)
) -> List[GitHubCommit]:
    """
    Obtém commits de um repositório.
    
    Args:
        owner: Proprietário do repositório
        repo: Nome do repositório
        page: Número da página (padrão: 1)
        per_page: Itens por página (padrão: 30, máximo: 100)
        
    Returns:
        Lista de commits do repositório
    """
    try:
        return await client.get_repository_commits(owner, repo, page, per_page)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erro ao buscar commits: {str(e)}")


@router.get("/repos/{owner}/{repo}/issues", response_model=List[GitHubIssue], summary="Obter issues do repositório", tags=["Repositórios"])
async def get_repository_issues(
    owner: str,
    repo: str,
    state: str = Query("open", description="Estado das issues (open/closed/all)"),
    page: int = Query(1, ge=1, description="Número da página"),
    per_page: int = Query(30, ge=1, le=100, description="Itens por página"),
    client: GitHubClient = Depends(get_github_client)
) -> List[GitHubIssue]:
    """
    Obtém issues de um repositório.
    
    Args:
        owner: Proprietário do repositório
        repo: Nome do repositório
        state: Estado das issues (open/closed/all)
        page: Número da página (padrão: 1)
        per_page: Itens por página (padrão: 30, máximo: 100)
        
    Returns:
        Lista de issues do repositório
    """
    try:
        return await client.get_repository_issues(owner, repo, state, page, per_page)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erro ao buscar issues: {str(e)}")


@router.get("/repos/{owner}/{repo}/pulls", response_model=List[GitHubPullRequest], summary="Obter Pull Requests do repositório", tags=["Repositórios"])
async def get_repository_pull_requests(
    owner: str,
    repo: str,
    state: str = Query("open", description="Estado dos PRs (open/closed/all)"),
    page: int = Query(1, ge=1, description="Número da página"),
    per_page: int = Query(30, ge=1, le=100, description="Itens por página"),
    client: GitHubClient = Depends(get_github_client)
) -> List[GitHubPullRequest]:
    """
    Obtém Pull Requests de um repositório.
    
    Args:
        owner: Proprietário do repositório
        repo: Nome do repositório
        state: Estado dos PRs (open/closed/all)
        page: Número da página (padrão: 1)
        per_page: Itens por página (padrão: 30, máximo: 100)
        
    Returns:
        Lista de Pull Requests do repositório
    """
    try:
        return await client.get_repository_pull_requests(owner, repo, state, page, per_page)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erro ao buscar Pull Requests: {str(e)}")


@router.get("/search/repositories", response_model=List[GitHubRepository], summary="Buscar repositórios", tags=["Busca"])
async def search_repositories(
    q: str = Query(..., description="Query de busca"),
    page: int = Query(1, ge=1, description="Número da página"),
    per_page: int = Query(30, ge=1, le=100, description="Itens por página"),
    client: GitHubClient = Depends(get_github_client)
) -> List[GitHubRepository]:
    """
    Busca repositórios no GitHub.
    
    Args:
        q: Query de busca
        page: Número da página (padrão: 1)
        per_page: Itens por página (padrão: 30, máximo: 100)
        
    Returns:
        Lista de repositórios encontrados
    """
    try:
        return await client.search_repositories(q, page, per_page)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro na busca: {str(e)}")


@router.get("/search/users", response_model=List[GitHubUser], summary="Buscar usuários", tags=["Busca"])
async def search_users(
    q: str = Query(..., description="Query de busca"),
    page: int = Query(1, ge=1, description="Número da página"),
    per_page: int = Query(30, ge=1, le=100, description="Itens por página"),
    client: GitHubClient = Depends(get_github_client)
) -> List[GitHubUser]:
    """
    Busca usuários no GitHub.
    
    Args:
        q: Query de busca
        page: Número da página (padrão: 1)
        per_page: Itens por página (padrão: 30, máximo: 100)
        
    Returns:
        Lista de usuários encontrados
    """
    try:
        return await client.search_users(q, page, per_page)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro na busca: {str(e)}")


@router.get("/health", summary="Verificar saúde da API", tags=["Sistema"])
async def health_check() -> dict:
    """
    ## 🔍 Health Check da API
    
    Verifica se a API está funcionando corretamente e retorna informações sobre o status do sistema.
    
    ### 📊 Informações Retornadas
    
    - **status**: Status da API (healthy/unhealthy)
    - **message**: Mensagem descritiva
    - **version**: Versão da API
    - **timestamp**: Timestamp da verificação
    - **cache**: Estatísticas do cache
    - **environment**: Ambiente (development/production)
    - **uptime**: Tempo de atividade em segundos
    - **memory**: Uso de memória
    - **github_api**: Status da API do GitHub
    
    ### 🔄 Uso
    
    ```bash
    curl https://github-data-api.onrender.com/api/v1/health
    ```
    
    ### 📝 Exemplo de Resposta
    
    ```json
    {
      "status": "healthy",
      "message": "GitHub Data API está funcionando corretamente",
      "version": "0.1.0",
      "timestamp": "2023-12-01T10:00:00",
      "cache": {
        "memory_cache_size": 1,
        "use_redis": false
      },
      "environment": "production",
      "uptime": 3600.5,
      "memory": {
        "rss": "45.2 MB",
        "heap": "12.8 MB"
      },
      "github_api": "connected"
    }
    ```
    
    Returns:
        dict: Status detalhado da API
    """
    from app.services.cache_service import cache_service
    from app.utils.logger import logger

    try:
        import psutil
        import time
        from app.services.github_client import GitHubClient
        
        # Verifica cache
        cache_stats = cache_service.get_stats()
        
        # Calcula uptime
        uptime = time.time() - psutil.boot_time()
        
        # Informações de memória
        process = psutil.Process()
        memory_info = process.memory_info()
        memory_stats = {
            "rss": f"{memory_info.rss / 1024 / 1024:.1f} MB",
            "heap": f"{memory_info.vms / 1024 / 1024:.1f} MB"
        }
        
        # Testa conexão com GitHub API
        github_status = "connected"
        try:
            client = GitHubClient()
            # Faz uma requisição simples para testar
            await client._make_request("/rate_limit")
        except Exception as e:
            github_status = f"error: {str(e)[:50]}"
            logger.warning(f"GitHub API não acessível: {e}")
        
        # Log de health check
        logger.info("Health check realizado", extra={
            "type": "health_check",
            "uptime": uptime,
            "memory_rss": memory_info.rss,
            "github_status": github_status
        })
        
        return {
            "status": "healthy",
            "message": "GitHub Data API está funcionando corretamente",
            "version": settings.api_version,
            "timestamp": datetime.now().isoformat(),
            "cache": cache_stats,
            "environment": "production" if not settings.debug else "development",
            "uptime": round(uptime, 2),
            "memory": memory_stats,
            "github_api": github_status
        }
    except Exception as e:
        logger.error(f"Health check falhou: {e}", extra={"type": "health_check_error"})
        return {
            "status": "unhealthy",
            "message": f"Erro na API: {str(e)}",
            "version": settings.api_version,
            "timestamp": datetime.now().isoformat()
        }


@router.get("/cache/stats", summary="Estatísticas do cache", tags=["Cache"])
async def cache_stats() -> dict:
    """
    ## 📊 Estatísticas do Cache
    
    Retorna informações detalhadas sobre o sistema de cache da API.
    
    ### 📈 Métricas Disponíveis
    
    - **memory_cache_size**: Número de itens em cache na memória
    - **memory_cache_maxsize**: Tamanho máximo do cache em memória
    - **use_redis**: Se o Redis está sendo usado
    - **redis_connected**: Status da conexão com Redis
    - **redis_used_memory**: Memória usada pelo Redis (se disponível)
    - **redis_keyspace_hits**: Hits do Redis (se disponível)
    - **redis_keyspace_misses**: Misses do Redis (se disponível)
    
    ### 🔄 Uso
    
    ```bash
    curl https://github-data-api.onrender.com/api/v1/cache/stats
    ```
    
    ### 📝 Exemplo de Resposta
    
    ```json
    {
      "memory_cache_size": 5,
      "memory_cache_maxsize": 1000,
      "use_redis": false,
      "redis_connected": false
    }
    ```
    
    Returns:
        dict: Estatísticas detalhadas do cache
    """
    from app.services.cache_service import cache_service
    return cache_service.get_stats()


@router.delete("/cache/clear", summary="Limpar cache", tags=["Cache"])
async def clear_cache() -> dict:
    """
    ## 🗑️ Limpar Cache
    
    Remove todos os dados armazenados no cache da API.
    
    ### ⚠️ Atenção
    
    Esta operação irá:
    - Limpar todo o cache em memória
    - Limpar todo o cache Redis (se configurado)
    - Forçar novas requisições à API do GitHub
    
    ### 🔄 Uso
    
    ```bash
    curl -X DELETE https://github-data-api.onrender.com/api/v1/cache/clear
    ```
    
    ### 📝 Exemplo de Resposta
    
    ```json
    {
      "success": true,
      "message": "Cache limpo com sucesso"
    }
    ```
    
    Returns:
        dict: Status da operação de limpeza
    """
    from app.services.cache_service import cache_service
    success = cache_service.clear()
    return {
        "success": success,
        "message": "Cache limpo com sucesso" if success else "Erro ao limpar cache"
    } 