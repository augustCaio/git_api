"""
Cliente HTTP para a API do GitHub
"""

import httpx
from typing import Optional, Dict, Any, List
from app.config import settings
from app.models.github_models import (
    GitHubUser,
    GitHubRepository,
    GitHubLanguage,
    GitHubEvent,
    GitHubCommit,
    GitHubIssue,
    GitHubPullRequest,
)
from app.services.cache_service import cache_service


class GitHubClient:
    """Cliente para interagir com a API do GitHub"""
    
    def __init__(self):
        self.base_url = settings.github_api_base_url
        self.token = settings.github_token
        self.headers = self._get_headers()
    
    def _get_headers(self) -> Dict[str, str]:
        """Retorna os headers para as requisições"""
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Data-API/0.1.0"
        }
        
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        
        return headers
    
    async def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Faz uma requisição para a API do GitHub"""
        url = f"{self.base_url}{endpoint}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
    
    async def get_user(self, username: str) -> GitHubUser:
        """Obtém dados de um usuário do GitHub"""
        cache_key = f"user:{username}"
        
        # Tenta obter do cache
        cached_data = cache_service.get(cache_key)
        if cached_data:
            return GitHubUser(**cached_data)
        
        # Busca da API
        data = await self._make_request(f"/users/{username}")
        
        # Armazena no cache (5 minutos)
        cache_service.set(cache_key, data, ttl=300)
        
        return GitHubUser(**data)
    
    async def get_user_repositories(self, username: str, page: int = 1, per_page: int = 30) -> List[GitHubRepository]:
        """Obtém repositórios de um usuário"""
        cache_key = f"user_repos:{username}:{page}:{per_page}"
        
        # Tenta obter do cache
        cached_data = cache_service.get(cache_key)
        if cached_data:
            return [GitHubRepository(**repo) for repo in cached_data]
        
        # Busca da API
        params = {"page": page, "per_page": per_page, "sort": "updated"}
        data = await self._make_request(f"/users/{username}/repos", params)
        
        # Armazena no cache (10 minutos)
        cache_service.set(cache_key, data, ttl=600)
        
        return [GitHubRepository(**repo) for repo in data]
    
    async def get_repository(self, owner: str, repo: str) -> GitHubRepository:
        """Obtém dados de um repositório específico"""
        data = await self._make_request(f"/repos/{owner}/{repo}")
        return GitHubRepository(**data)
    
    async def get_repository_languages(self, owner: str, repo: str) -> Dict[str, GitHubLanguage]:
        """Obtém as linguagens de programação de um repositório"""
        data = await self._make_request(f"/repos/{owner}/{repo}/languages")
        
        # Calcula o total de bytes
        total_bytes = sum(data.values())
        
        # Cria os objetos GitHubLanguage com porcentagens
        languages = {}
        for name, bytes_count in data.items():
            percentage = (bytes_count / total_bytes) * 100 if total_bytes > 0 else 0
            languages[name] = GitHubLanguage(
                name=name,
                bytes=bytes_count,
                percentage=round(percentage, 2)
            )
        
        return languages
    
    async def get_repository_events(self, owner: str, repo: str, page: int = 1, per_page: int = 30) -> List[GitHubEvent]:
        """Obtém eventos de um repositório"""
        params = {"page": page, "per_page": per_page}
        data = await self._make_request(f"/repos/{owner}/{repo}/events", params)
        return [GitHubEvent(**event) for event in data]
    
    async def get_repository_commits(self, owner: str, repo: str, page: int = 1, per_page: int = 30) -> List[GitHubCommit]:
        """Obtém commits de um repositório"""
        params = {"page": page, "per_page": per_page}
        data = await self._make_request(f"/repos/{owner}/{repo}/commits", params)
        return [GitHubCommit(**commit) for commit in data]
    
    async def get_repository_issues(self, owner: str, repo: str, state: str = "open", page: int = 1, per_page: int = 30) -> List[GitHubIssue]:
        """Obtém issues de um repositório"""
        params = {"state": state, "page": page, "per_page": per_page}
        data = await self._make_request(f"/repos/{owner}/{repo}/issues", params)
        return [GitHubIssue(**issue) for issue in data]
    
    async def get_repository_pull_requests(self, owner: str, repo: str, state: str = "open", page: int = 1, per_page: int = 30) -> List[GitHubPullRequest]:
        """Obtém Pull Requests de um repositório"""
        params = {"state": state, "page": page, "per_page": per_page}
        data = await self._make_request(f"/repos/{owner}/{repo}/pulls", params)
        return [GitHubPullRequest(**pr) for pr in data]
    
    async def search_repositories(self, query: str, page: int = 1, per_page: int = 30) -> List[GitHubRepository]:
        """Busca repositórios no GitHub"""
        params = {"q": query, "page": page, "per_page": per_page, "sort": "stars"}
        data = await self._make_request("/search/repositories", params)
        return [GitHubRepository(**repo) for repo in data.get("items", [])]
    
    async def search_users(self, query: str, page: int = 1, per_page: int = 30) -> List[GitHubUser]:
        """Busca usuários no GitHub"""
        params = {"q": query, "page": page, "per_page": per_page}
        data = await self._make_request("/search/users", params)
        return [GitHubUser(**user) for user in data.get("items", [])]
    
    async def get_user_languages(self, username: str) -> Dict[str, GitHubLanguage]:
        """Obtém as linguagens de programação mais usadas por um usuário"""
        # Primeiro, obtém todos os repositórios do usuário
        repos = await self.get_user_repositories(username, page=1, per_page=100)
        
        # Agrupa as linguagens de todos os repositórios
        language_stats = {}
        
        for repo in repos:
            if repo.language:
                if repo.language not in language_stats:
                    language_stats[repo.language] = {
                        "name": repo.language,
                        "bytes": 0,
                        "repos_count": 0,
                        "total_stars": 0
                    }
                
                language_stats[repo.language]["repos_count"] += 1
                language_stats[repo.language]["total_stars"] += repo.stargazers_count
        
        # Converte para objetos GitHubLanguage
        languages = {}
        for lang_name, stats in language_stats.items():
            languages[lang_name] = GitHubLanguage(
                name=stats["name"],
                bytes=stats["bytes"],
                percentage=stats["repos_count"]  # Usa contagem de repositórios como porcentagem
            )
        
        return languages
    
    async def get_user_stats(self, username: str) -> Dict[str, Any]:
        """Obtém estatísticas detalhadas de um usuário"""
        # Obtém dados do usuário
        user = await self.get_user(username)
        
        # Obtém repositórios
        repos = await self.get_user_repositories(username, page=1, per_page=100)
        
        # Calcula estatísticas
        total_stars = sum(repo.stargazers_count for repo in repos)
        total_forks = sum(repo.forks_count for repo in repos)
        total_issues = sum(repo.open_issues_count for repo in repos)
        
        # Conta repositórios por tipo
        public_repos = len([repo for repo in repos if not repo.private])
        private_repos = len([repo for repo in repos if repo.private])
        forked_repos = len([repo for repo in repos if repo.fork])
        original_repos = len([repo for repo in repos if not repo.fork])
        
        # Top linguagens
        languages = {}
        for repo in repos:
            if repo.language:
                if repo.language not in languages:
                    languages[repo.language] = 0
                languages[repo.language] += 1
        
        top_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Repositórios mais populares
        top_repos = sorted(repos, key=lambda x: x.stargazers_count, reverse=True)[:5]
        
        return {
            "user": user,
            "repositories": {
                "total": len(repos),
                "public": public_repos,
                "private": private_repos,
                "forked": forked_repos,
                "original": original_repos
            },
            "activity": {
                "total_stars": total_stars,
                "total_forks": total_forks,
                "total_issues": total_issues,
                "average_stars_per_repo": round(total_stars / len(repos), 2) if repos else 0
            },
            "languages": {
                "top_languages": [{"language": lang, "count": count} for lang, count in top_languages],
                "total_languages": len(languages)
            },
            "top_repositories": [
                {
                    "name": repo.name,
                    "full_name": repo.full_name,
                    "description": repo.description,
                    "stars": repo.stargazers_count,
                    "forks": repo.forks_count,
                    "language": repo.language
                }
                for repo in top_repos
            ]
        } 