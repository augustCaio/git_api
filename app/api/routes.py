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
    curl https://git-api-i3y5.onrender.com/api/v1/users/octocat
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


@router.get("/users/{username}/repositories", response_model=List[GitHubRepository], summary="Obter todos os repositórios do usuário", tags=["Usuários"])
async def get_user_repositories(
    username: str,
    page: int = Query(1, ge=1, description="Número da página"),
    per_page: int = Query(30, ge=1, le=100, description="Itens por página"),
    client: GitHubClient = Depends(get_github_client)
) -> List[GitHubRepository]:
    """
    ## 📚 Todos os Repositórios do Usuário
    
    Obtém **todos os repositórios** de um usuário do GitHub, incluindo:
    
    - ✅ **Repositórios públicos** (visíveis para todos)
    - ✅ **Repositórios privados** (se você tiver acesso)
    - ✅ **Repositórios forkados** (criados a partir de outros)
    - ✅ **Repositórios originais** (criados pelo usuário)
    
    ### 📊 Dados Retornados
    
    Para cada repositório:
    - **Informações básicas**: Nome, descrição, linguagem principal
    - **Estatísticas**: Stars, forks, issues, watchers
    - **Configurações**: Privado/público, fork, arquivado
    - **Metadados**: Data de criação, última atualização, tamanho
    - **Links**: URL do repositório, homepage, documentação
    
    ### 🔄 Uso
    
    ```bash
    # Todos os repositórios (primeira página)
    curl https://git-api-i3y5.onrender.com/api/v1/users/augustcaio/repositories
    
    # Com paginação
    curl https://git-api-i3y5.onrender.com/api/v1/users/augustcaio/repositories?page=1&per_page=50
    
    # Máximo de repositórios por página
    curl https://git-api-i3y5.onrender.com/api/v1/users/augustcaio/repositories?per_page=100
    ```
    
    ### 📝 Exemplo de Resposta
    
    ```json
    [
      {
        "id": 1031918183,
        "name": "portfolio-2025",
        "full_name": "augustcaio/portfolio-2025",
        "description": "Meu portfólio pessoal 2025",
        "private": false,
        "fork": false,
        "language": "TypeScript",
        "size": 1024,
        "stargazers_count": 5,
        "watchers_count": 5,
        "forks_count": 2,
        "open_issues_count": 1,
        "default_branch": "main",
        "created_at": "2025-01-15T10:30:00Z",
        "updated_at": "2025-07-29T16:00:00Z"
      },
      {
        "id": 1028484319,
        "name": "git_api",
        "full_name": "augustcaio/git_api",
        "description": "API para dados do GitHub",
        "private": false,
        "fork": false,
        "language": "Python",
        "size": 2048,
        "stargazers_count": 10,
        "watchers_count": 10,
        "forks_count": 3,
        "open_issues_count": 0,
        "default_branch": "main",
        "created_at": "2025-01-10T14:20:00Z",
        "updated_at": "2025-07-29T15:30:00Z"
      }
    ]
    ```
    
    ### ⚙️ Parâmetros
    
    - **username** (obrigatório): Nome do usuário no GitHub
    - **page** (opcional): Número da página (padrão: 1)
    - **per_page** (opcional): Itens por página (padrão: 30, máximo: 100)
    
    ### ⚠️ Limitações
    
    - **Rate limit**: 60 requisições/hora (sem token) / 5000 requisições/hora (com token)
    - **Cache**: Dados em cache por 10 minutos para melhor performance
    - **Repositórios privados**: Só aparecem se você tiver acesso (com token)
    - **Ordenação**: Repositórios ordenados por data de atualização (mais recentes primeiro)
    
    ### 🔗 Endpoints Relacionados
    
    - `GET /users/{username}` - Dados do usuário
    - `GET /users/{username}/languages` - Linguagens mais usadas
    - `GET /users/{username}/stats` - Estatísticas completas
    - `GET /repos/{owner}/{repo}` - Dados de um repositório específico
    
    Args:
        username (str): Nome do usuário no GitHub
        page (int): Número da página (padrão: 1)
        per_page (int): Itens por página (padrão: 30, máximo: 100)
        
    Returns:
        List[GitHubRepository]: Lista completa de repositórios do usuário
    """
    try:
        return await client.get_user_repositories(username, page, per_page)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erro ao buscar repositórios: {str(e)}")


@router.get("/users/{username}/repositories/summary", summary="Resumo de todos os repositórios do usuário", tags=["Usuários"])
async def get_user_repositories_summary(
    username: str,
    client: GitHubClient = Depends(get_github_client)
) -> dict:
    """
    ## 📊 Resumo Completo dos Repositórios
    
    Obtém um **resumo estatístico** de todos os repositórios de um usuário, incluindo:
    
    - 📈 **Estatísticas gerais**: Total de repositórios, stars, forks
    - 🗣️ **Linguagens mais usadas**: Ranking das linguagens de programação
    - 📅 **Atividade recente**: Repositórios mais atualizados
    - ⭐ **Repositórios populares**: Com mais stars e forks
    - 🔒 **Visibilidade**: Distribuição entre públicos e privados
    
    ### 📊 Dados Retornados
    
    ```json
    {
      "username": "augustcaio",
      "summary": {
        "total_repositories": 5,
        "public_repositories": 4,
        "private_repositories": 1,
        "total_stars": 25,
        "total_forks": 8,
        "total_watchers": 30,
        "total_size": 10240
      },
      "languages": {
        "Python": {"count": 2, "percentage": 40.0},
        "TypeScript": {"count": 1, "percentage": 20.0},
        "JavaScript": {"count": 1, "percentage": 20.0}
      },
      "top_repositories": [
        {
          "name": "git_api",
          "stars": 10,
          "forks": 3,
          "language": "Python"
        }
      ],
      "recent_activity": [
        {
          "name": "portfolio-2025",
          "updated_at": "2025-07-29T16:00:00Z",
          "language": "TypeScript"
        }
      ]
    }
    ```
    
    ### 🔄 Uso
    
    ```bash
    curl https://git-api-i3y5.onrender.com/api/v1/users/augustcaio/repositories/summary
    ```
    
    ### ⚠️ Limitações
    
    - **Rate limit**: 60 requisições/hora (sem token) / 5000 requisições/hora (com token)
    - **Cache**: Dados em cache por 15 minutos para melhor performance
    - **Repositórios privados**: Só aparecem se você tiver acesso (com token)
    
    Args:
        username (str): Nome do usuário no GitHub
        
    Returns:
        dict: Resumo estatístico completo dos repositórios
    """
    try:
        # Obtém todos os repositórios (máximo 100 por página)
        all_repos = await client.get_user_repositories(username, page=1, per_page=100)
        
        if not all_repos:
            return {
                "username": username,
                "summary": {
                    "total_repositories": 0,
                    "public_repositories": 0,
                    "private_repositories": 0,
                    "total_stars": 0,
                    "total_forks": 0,
                    "total_watchers": 0,
                    "total_size": 0
                },
                "languages": {},
                "top_repositories": [],
                "recent_activity": []
            }
        
        # Calcula estatísticas
        total_repos = len(all_repos)
        public_repos = len([r for r in all_repos if not r.private])
        private_repos = len([r for r in all_repos if r.private])
        total_stars = sum(r.stargazers_count for r in all_repos)
        total_forks = sum(r.forks_count for r in all_repos)
        total_watchers = sum(r.watchers_count for r in all_repos)
        total_size = sum(r.size for r in all_repos)
        
        # Análise de linguagens
        languages = {}
        for repo in all_repos:
            if repo.language:
                if repo.language not in languages:
                    languages[repo.language] = {"count": 0, "percentage": 0}
                languages[repo.language]["count"] += 1
        
        # Calcula porcentagens
        for lang in languages:
            languages[lang]["percentage"] = (languages[lang]["count"] / total_repos) * 100
        
        # Top repositórios (por stars)
        top_repos = sorted(all_repos, key=lambda x: x.stargazers_count, reverse=True)[:5]
        top_repos_data = [
            {
                "name": repo.name,
                "full_name": repo.full_name,
                "stars": repo.stargazers_count,
                "forks": repo.forks_count,
                "language": repo.language,
                "description": repo.description
            }
            for repo in top_repos
        ]
        
        # Atividade recente
        recent_repos = sorted(all_repos, key=lambda x: x.updated_at or datetime.min, reverse=True)[:5]
        recent_activity = [
            {
                "name": repo.name,
                "full_name": repo.full_name,
                "updated_at": repo.updated_at.isoformat() if repo.updated_at else None,
                "language": repo.language,
                "description": repo.description
            }
            for repo in recent_repos
        ]
        
        return {
            "username": username,
            "summary": {
                "total_repositories": total_repos,
                "public_repositories": public_repos,
                "private_repositories": private_repos,
                "total_stars": total_stars,
                "total_forks": total_forks,
                "total_watchers": total_watchers,
                "total_size": total_size
            },
            "languages": languages,
            "top_repositories": top_repos_data,
            "recent_activity": recent_activity
        }
        
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Erro ao buscar resumo dos repositórios: {str(e)}")


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
    curl https://git-api-i3y5.onrender.com/api/v1/health
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
    curl https://git-api-i3y5.onrender.com/api/v1/cache/stats
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
    curl -X DELETE https://git-api-i3y5.onrender.com/api/v1/cache/clear
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