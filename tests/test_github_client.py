"""
Testes para o cliente GitHub
"""

import pytest
import httpx
from unittest.mock import AsyncMock, patch, MagicMock
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


@pytest.fixture
def github_client():
    """Fixture para criar um cliente GitHub"""
    return GitHubClient()


@pytest.fixture
def mock_response():
    """Fixture para mock de resposta HTTP"""
    mock = MagicMock()
    mock.json.return_value = {
        "id": 583231,
        "login": "octocat",
        "name": "The Octocat",
        "email": None,
        "avatar_url": "https://avatars.githubusercontent.com/u/583231?v=4",
        "bio": None,
        "location": "San Francisco",
        "company": "@github",
        "public_repos": 8,
        "public_gists": 8,
        "followers": 1000,
        "following": 9,
        "type": "User",
        "site_admin": False
    }
    return mock


class TestGitHubClientInitialization:
    """Testes para inicialização do cliente GitHub"""
    
    def test_github_client_initialization(self, github_client):
        """Testa a inicialização do cliente GitHub"""
        assert github_client.base_url == "https://api.github.com"
        assert "Accept" in github_client.headers
        assert "User-Agent" in github_client.headers
        assert github_client.headers["Accept"] == "application/vnd.github.v3+json"
        assert github_client.headers["User-Agent"] == "GitHub-Data-API/0.1.0"
    
    def test_github_client_headers_with_token(self):
        """Testa os headers quando um token está presente"""
        # Simula um token
        client = GitHubClient()
        client.token = "test_token"
        headers = client._get_headers()
        
        assert "Authorization" in headers
        assert headers["Authorization"] == "token test_token"
    
    def test_github_client_headers_without_token(self):
        """Testa os headers quando não há token"""
        client = GitHubClient()
        client.token = None
        headers = client._get_headers()
        
        assert "Authorization" not in headers
        assert "Accept" in headers
        assert "User-Agent" in headers


class TestGitHubClientRequests:
    """Testes para requisições do cliente GitHub"""
    
    @pytest.mark.asyncio
    @patch('httpx.AsyncClient.get')
    async def test_make_request_success(self, mock_get, github_client, mock_response):
        """Testa requisição bem-sucedida"""
        mock_get.return_value = mock_response
        
        result = await github_client._make_request("/users/octocat")
        
        assert result["login"] == "octocat"
        assert result["name"] == "The Octocat"
        mock_get.assert_called_once()
    
    @pytest.mark.asyncio
    @patch('httpx.AsyncClient.get')
    async def test_make_request_with_params(self, mock_get, github_client, mock_response):
        """Testa requisição com parâmetros"""
        mock_get.return_value = mock_response
        
        params = {"page": 1, "per_page": 30}
        await github_client._make_request("/users/octocat/repos", params)
        
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert call_args[1]["params"] == params
    
    @pytest.mark.asyncio
    @patch('httpx.AsyncClient.get')
    async def test_make_request_error(self, mock_get, github_client):
        """Testa requisição com erro"""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "404 Not Found", request=MagicMock(), response=MagicMock()
        )
        mock_get.return_value = mock_response
        
        with pytest.raises(httpx.HTTPStatusError):
            await github_client._make_request("/users/nonexistent")


class TestGitHubClientUserMethods:
    """Testes para métodos de usuário"""
    
    @pytest.mark.asyncio
    @patch.object(GitHubClient, '_make_request')
    async def test_get_user_success(self, mock_make_request, github_client):
        """Testa obtenção de usuário com sucesso"""
        mock_data = {
            "id": 583231,
            "login": "octocat",
            "name": "The Octocat",
            "email": None,
            "avatar_url": "https://avatars.githubusercontent.com/u/583231?v=4",
            "bio": None,
            "location": "San Francisco",
            "company": "@github",
            "public_repos": 8,
            "public_gists": 8,
            "followers": 1000,
            "following": 9,
            "type": "User",
            "site_admin": False
        }
        mock_make_request.return_value = mock_data
        
        result = await github_client.get_user("octocat")
        
        assert isinstance(result, GitHubUser)
        assert result.login == "octocat"
        assert result.name == "The Octocat"
        assert result.id == 583231
        mock_make_request.assert_called_once_with("/users/octocat")
    
    @pytest.mark.asyncio
    @patch.object(GitHubClient, '_make_request')
    async def test_get_user_repositories_success(self, mock_make_request, github_client):
        """Testa obtenção de repositórios de usuário"""
        mock_data = [
            {
                "id": 1,
                "name": "test-repo",
                "full_name": "octocat/test-repo",
                "description": "Test repository",
                "private": False,
                "fork": False,
                "language": "Python",
                "size": 100,
                "stargazers_count": 10,
                "watchers_count": 10,
                "forks_count": 5,
                "open_issues_count": 2,
                "default_branch": "main",
                "topics": ["test", "python"]
            }
        ]
        mock_make_request.return_value = mock_data
        
        result = await github_client.get_user_repositories("octocat")
        
        assert len(result) == 1
        assert isinstance(result[0], GitHubRepository)
        assert result[0].name == "test-repo"
        assert result[0].language == "Python"
        mock_make_request.assert_called_once_with(
            "/users/octocat/repos", 
            {"page": 1, "per_page": 30, "sort": "updated"}
        )


class TestGitHubClientRepositoryMethods:
    """Testes para métodos de repositório"""
    
    @pytest.mark.asyncio
    @patch.object(GitHubClient, '_make_request')
    async def test_get_repository_success(self, mock_make_request, github_client):
        """Testa obtenção de repositório"""
        mock_data = {
            "id": 1,
            "name": "test-repo",
            "full_name": "octocat/test-repo",
            "description": "Test repository",
            "private": False,
            "fork": False,
            "language": "Python",
            "size": 100,
            "stargazers_count": 10,
            "watchers_count": 10,
            "forks_count": 5,
            "open_issues_count": 2,
            "default_branch": "main"
        }
        mock_make_request.return_value = mock_data
        
        result = await github_client.get_repository("octocat", "test-repo")
        
        assert isinstance(result, GitHubRepository)
        assert result.name == "test-repo"
        assert result.full_name == "octocat/test-repo"
        assert result.language == "Python"
        mock_make_request.assert_called_once_with("/repos/octocat/test-repo")
    
    @pytest.mark.asyncio
    @patch.object(GitHubClient, '_make_request')
    async def test_get_repository_languages_success(self, mock_make_request, github_client):
        """Testa obtenção de linguagens de repositório"""
        mock_data = {
            "Python": 1000,
            "JavaScript": 400,
            "HTML": 300
        }
        mock_make_request.return_value = mock_data
        
        result = await github_client.get_repository_languages("octocat", "test-repo")
        
        assert len(result) == 3
        assert "Python" in result
        assert "JavaScript" in result
        assert "HTML" in result
        
        # Verifica se as porcentagens foram calculadas corretamente
        total_bytes = 1000 + 400 + 300
        assert result["Python"].percentage == pytest.approx(58.82, rel=0.01)
        assert result["JavaScript"].percentage == pytest.approx(23.53, rel=0.01)
        assert result["HTML"].percentage == pytest.approx(17.65, rel=0.01)
        
        mock_make_request.assert_called_once_with("/repos/octocat/test-repo/languages")
    
    @pytest.mark.asyncio
    @patch.object(GitHubClient, '_make_request')
    async def test_get_repository_events_success(self, mock_make_request, github_client):
        """Testa obtenção de eventos de repositório"""
        mock_data = [
            {
                "id": "123",
                "type": "PushEvent",
                "public": True,
                "repo": {"id": 1, "name": "octocat/test-repo"}
            }
        ]
        mock_make_request.return_value = mock_data
        
        result = await github_client.get_repository_events("octocat", "test-repo")
        
        assert len(result) == 1
        assert isinstance(result[0], GitHubEvent)
        assert result[0].type == "PushEvent"
        mock_make_request.assert_called_once_with(
            "/repos/octocat/test-repo/events",
            {"page": 1, "per_page": 30}
        )
    
    @pytest.mark.asyncio
    @patch.object(GitHubClient, '_make_request')
    async def test_get_repository_commits_success(self, mock_make_request, github_client):
        """Testa obtenção de commits de repositório"""
        mock_data = [
            {
                "sha": "abc123",
                "node_id": "MDY6Q29tbWl0MTIz",
                "commit": {"message": "Initial commit"},
                "url": "https://api.github.com/repos/octocat/test-repo/commits/abc123",
                "html_url": "https://github.com/octocat/test-repo/commit/abc123",
                "comments_url": "https://api.github.com/repos/octocat/test-repo/commits/abc123/comments"
            }
        ]
        mock_make_request.return_value = mock_data
        
        result = await github_client.get_repository_commits("octocat", "test-repo")
        
        assert len(result) == 1
        assert isinstance(result[0], GitHubCommit)
        assert result[0].sha == "abc123"
        mock_make_request.assert_called_once_with(
            "/repos/octocat/test-repo/commits",
            {"page": 1, "per_page": 30}
        )


class TestGitHubClientIssuesAndPRs:
    """Testes para issues e Pull Requests"""
    
    @pytest.mark.asyncio
    @patch.object(GitHubClient, '_make_request')
    async def test_get_repository_issues_success(self, mock_make_request, github_client):
        """Testa obtenção de issues"""
        mock_data = [
            {
                "id": 1,
                "number": 1,
                "title": "Test Issue",
                "body": "This is a test issue",
                "state": "open",
                "locked": False,
                "comments": 0,
                "author_association": "NONE",
                "labels": []
            }
        ]
        mock_make_request.return_value = mock_data
        
        result = await github_client.get_repository_issues("octocat", "test-repo")
        
        assert len(result) == 1
        assert isinstance(result[0], GitHubIssue)
        assert result[0].title == "Test Issue"
        assert result[0].state == "open"
        mock_make_request.assert_called_once_with(
            "/repos/octocat/test-repo/issues",
            {"state": "open", "page": 1, "per_page": 30}
        )
    
    @pytest.mark.asyncio
    @patch.object(GitHubClient, '_make_request')
    async def test_get_repository_pull_requests_success(self, mock_make_request, github_client):
        """Testa obtenção de Pull Requests"""
        mock_data = [
            {
                "id": 1,
                "number": 1,
                "title": "Test PR",
                "body": "This is a test PR",
                "state": "open",
                "locked": False,
                "comments": 0,
                "review_comments": 0,
                "commits": 1,
                "additions": 10,
                "deletions": 5,
                "changed_files": 2,
                "author_association": "NONE",
                "labels": [],
                "head": {"ref": "feature-branch"},
                "base": {"ref": "main"},
                "draft": False,
                "merged": False,
                "mergeable": None,
                "mergeable_state": "unknown",
                "comments_url": "https://api.github.com/repos/octocat/test-repo/issues/1/comments",
                "review_comments_url": "https://api.github.com/repos/octocat/test-repo/pulls/1/comments",
                "commits_url": "https://api.github.com/repos/octocat/test-repo/pulls/1/commits",
                "statuses_url": "https://api.github.com/repos/octocat/test-repo/statuses/abc123"
            }
        ]
        mock_make_request.return_value = mock_data
        
        result = await github_client.get_repository_pull_requests("octocat", "test-repo")
        
        assert len(result) == 1
        assert isinstance(result[0], GitHubPullRequest)
        assert result[0].title == "Test PR"
        assert result[0].state == "open"
        mock_make_request.assert_called_once_with(
            "/repos/octocat/test-repo/pulls",
            {"state": "open", "page": 1, "per_page": 30}
        )


class TestGitHubClientSearchMethods:
    """Testes para métodos de busca"""
    
    @pytest.mark.asyncio
    @patch.object(GitHubClient, '_make_request')
    async def test_search_repositories_success(self, mock_make_request, github_client):
        """Testa busca de repositórios"""
        mock_data = {
            "items": [
                {
                    "id": 1,
                    "name": "test-repo",
                    "full_name": "octocat/test-repo",
                    "description": "Test repository",
                    "private": False,
                    "fork": False,
                    "language": "Python",
                    "size": 100,
                    "stargazers_count": 10,
                    "watchers_count": 10,
                    "forks_count": 5,
                    "open_issues_count": 2,
                    "default_branch": "main"
                }
            ]
        }
        mock_make_request.return_value = mock_data
        
        result = await github_client.search_repositories("python")
        
        assert len(result) == 1
        assert isinstance(result[0], GitHubRepository)
        assert result[0].language == "Python"
        mock_make_request.assert_called_once_with(
            "/search/repositories",
            {"q": "python", "page": 1, "per_page": 30, "sort": "stars"}
        )
    
    @pytest.mark.asyncio
    @patch.object(GitHubClient, '_make_request')
    async def test_search_users_success(self, mock_make_request, github_client):
        """Testa busca de usuários"""
        mock_data = {
            "items": [
                {
                    "id": 1,
                    "login": "testuser",
                    "name": "Test User",
                    "email": None,
                    "public_repos": 5,
                    "public_gists": 2,
                    "followers": 10,
                    "following": 5,
                    "type": "User",
                    "site_admin": False
                }
            ]
        }
        mock_make_request.return_value = mock_data
        
        result = await github_client.search_users("testuser")
        
        assert len(result) == 1
        assert isinstance(result[0], GitHubUser)
        assert result[0].login == "testuser"
        mock_make_request.assert_called_once_with(
            "/search/users",
            {"q": "testuser", "page": 1, "per_page": 30}
        )


class TestGitHubClientErrorHandling:
    """Testes para tratamento de erros"""
    
    @pytest.mark.asyncio
    @patch.object(GitHubClient, '_make_request')
    async def test_get_user_not_found(self, mock_make_request, github_client):
        """Testa usuário não encontrado"""
        mock_make_request.side_effect = httpx.HTTPStatusError(
            "404 Not Found", request=MagicMock(), response=MagicMock()
        )
        
        with pytest.raises(httpx.HTTPStatusError):
            await github_client.get_user("nonexistent")
    
    @pytest.mark.asyncio
    @patch.object(GitHubClient, '_make_request')
    async def test_get_repository_not_found(self, mock_make_request, github_client):
        """Testa repositório não encontrado"""
        mock_make_request.side_effect = httpx.HTTPStatusError(
            "404 Not Found", request=MagicMock(), response=MagicMock()
        )
        
        with pytest.raises(httpx.HTTPStatusError):
            await github_client.get_repository("octocat", "nonexistent")


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 