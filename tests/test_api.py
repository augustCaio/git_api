"""
Testes automatizados completos para a GitHub Data API
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock
from app.main import app
from app.models.github_models import (
    GitHubUser,
    GitHubRepository,
    GitHubLanguage,
    GitHubEvent,
    GitHubCommit,
    GitHubIssue,
    GitHubPullRequest,
)

# Cliente de teste
client = TestClient(app)


class TestHealthEndpoint:
    """Testes para o endpoint de saúde da API"""
    
    def test_health_check(self):
        """Testa o endpoint de saúde da API"""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "funcionando corretamente" in data["message"]


class TestRootEndpoint:
    """Testes para o endpoint raiz"""
    
    def test_root_endpoint(self):
        """Testa o endpoint raiz da API"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Bem-vindo à GitHub Data API"
        assert data["version"] == "0.1.0"
        assert "/docs" in data["docs"]
        assert "/api/v1/health" in data["health"]


class TestUserEndpoints:
    """Testes para endpoints de usuários"""
    
    @patch('app.services.github_client.GitHubClient.get_user')
    def test_get_user_success(self, mock_get_user):
        """Testa obtenção de dados de usuário com sucesso"""
        # Mock do usuário
        mock_user = GitHubUser(
            id=583231,
            login="octocat",
            name="The Octocat",
            email=None,
            avatar_url="https://avatars.githubusercontent.com/u/583231?v=4",
            bio=None,
            location="San Francisco",
            company="@github",
            public_repos=8,
            public_gists=8,
            followers=1000,
            following=9,
            type="User",
            site_admin=False
        )
        mock_get_user.return_value = mock_user
        
        response = client.get("/api/v1/users/octocat")
        assert response.status_code == 200
        data = response.json()
        assert data["login"] == "octocat"
        assert data["name"] == "The Octocat"
        assert data["id"] == 583231
    
    @patch('app.services.github_client.GitHubClient.get_user')
    def test_get_user_not_found(self, mock_get_user):
        """Testa obtenção de usuário inexistente"""
        mock_get_user.side_effect = Exception("User not found")
        
        response = client.get("/api/v1/users/nonexistent")
        assert response.status_code == 404
        data = response.json()
        assert "não encontrado" in data["detail"]
    
    @patch('app.services.github_client.GitHubClient.get_user_repositories')
    def test_get_user_repositories_success(self, mock_get_repos):
        """Testa obtenção de repositórios de usuário com sucesso"""
        # Mock dos repositórios
        mock_repos = [
            GitHubRepository(
                id=1,
                name="test-repo",
                full_name="octocat/test-repo",
                description="Test repository",
                private=False,
                fork=False,
                language="Python",
                size=100,
                stargazers_count=10,
                watchers_count=10,
                forks_count=5,
                open_issues_count=2,
                default_branch="main",
                topics=["test", "python"]
            )
        ]
        mock_get_repos.return_value = mock_repos
        
        response = client.get("/api/v1/users/octocat/repositories")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "test-repo"
        assert data[0]["language"] == "Python"
    
    @patch('app.services.github_client.GitHubClient.get_user_repositories')
    def test_get_user_repositories_with_pagination(self, mock_get_repos):
        """Testa paginação de repositórios"""
        mock_get_repos.return_value = []
        
        response = client.get("/api/v1/users/octocat/repositories?page=2&per_page=10")
        assert response.status_code == 200
        mock_get_repos.assert_called_once_with("octocat", 2, 10)


class TestRepositoryEndpoints:
    """Testes para endpoints de repositórios"""
    
    @patch('app.services.github_client.GitHubClient.get_repository')
    def test_get_repository_success(self, mock_get_repo):
        """Testa obtenção de dados de repositório com sucesso"""
        mock_repo = GitHubRepository(
            id=1,
            name="test-repo",
            full_name="octocat/test-repo",
            description="Test repository",
            private=False,
            fork=False,
            language="Python",
            size=100,
            stargazers_count=10,
            watchers_count=10,
            forks_count=5,
            open_issues_count=2,
            default_branch="main"
        )
        mock_get_repo.return_value = mock_repo
        
        response = client.get("/api/v1/repos/octocat/test-repo")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "test-repo"
        assert data["full_name"] == "octocat/test-repo"
        assert data["language"] == "Python"
    
    @patch('app.services.github_client.GitHubClient.get_repository')
    def test_get_repository_not_found(self, mock_get_repo):
        """Testa obtenção de repositório inexistente"""
        mock_get_repo.side_effect = Exception("Repository not found")
        
        response = client.get("/api/v1/repos/octocat/nonexistent")
        assert response.status_code == 404
        data = response.json()
        assert "não encontrado" in data["detail"]
    
    @patch('app.services.github_client.GitHubClient.get_repository_languages')
    def test_get_repository_languages_success(self, mock_get_languages):
        """Testa obtenção de linguagens de repositório"""
        mock_languages = {
            "Python": GitHubLanguage(name="Python", bytes=1000, percentage=60.0),
            "JavaScript": GitHubLanguage(name="JavaScript", bytes=400, percentage=24.0),
            "HTML": GitHubLanguage(name="HTML", bytes=300, percentage=16.0)
        }
        mock_get_languages.return_value = mock_languages
        
        response = client.get("/api/v1/repos/octocat/test-repo/languages")
        assert response.status_code == 200
        data = response.json()
        assert data["repository"] == "octocat/test-repo"
        assert data["total_languages"] == 3
        assert "Python" in data["languages"]
        assert data["languages"]["Python"]["percentage"] == 60.0
    
    @patch('app.services.github_client.GitHubClient.get_repository_events')
    def test_get_repository_events_success(self, mock_get_events):
        """Testa obtenção de eventos de repositório"""
        mock_events = [
            GitHubEvent(
                id="123",
                type="PushEvent",
                public=True,
                repo={"id": 1, "name": "octocat/test-repo"}
            )
        ]
        mock_get_events.return_value = mock_events
        
        response = client.get("/api/v1/repos/octocat/test-repo/events")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["type"] == "PushEvent"
    
    @patch('app.services.github_client.GitHubClient.get_repository_commits')
    def test_get_repository_commits_success(self, mock_get_commits):
        """Testa obtenção de commits de repositório"""
        mock_commits = [
            GitHubCommit(
                sha="abc123",
                node_id="MDY6Q29tbWl0MTIz",
                commit={"message": "Initial commit"},
                url="https://api.github.com/repos/octocat/test-repo/commits/abc123",
                html_url="https://github.com/octocat/test-repo/commit/abc123",
                comments_url="https://api.github.com/repos/octocat/test-repo/commits/abc123/comments"
            )
        ]
        mock_get_commits.return_value = mock_commits
        
        response = client.get("/api/v1/repos/octocat/test-repo/commits")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["sha"] == "abc123"
    
    @patch('app.services.github_client.GitHubClient.get_repository_issues')
    def test_get_repository_issues_success(self, mock_get_issues):
        """Testa obtenção de issues de repositório"""
        mock_issues = [
            GitHubIssue(
                id=1,
                number=1,
                title="Test Issue",
                body="This is a test issue",
                state="open",
                locked=False,
                comments=0,
                author_association="NONE",
                labels=[]
            )
        ]
        mock_get_issues.return_value = mock_issues
        
        response = client.get("/api/v1/repos/octocat/test-repo/issues")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Test Issue"
        assert data[0]["state"] == "open"
    
    @patch('app.services.github_client.GitHubClient.get_repository_issues')
    def test_get_repository_issues_with_state(self, mock_get_issues):
        """Testa obtenção de issues com filtro de estado"""
        mock_get_issues.return_value = []
        
        response = client.get("/api/v1/repos/octocat/test-repo/issues?state=closed")
        assert response.status_code == 200
        mock_get_issues.assert_called_once_with("octocat", "test-repo", "closed", 1, 30)
    
    @patch('app.services.github_client.GitHubClient.get_repository_pull_requests')
    def test_get_repository_pull_requests_success(self, mock_get_prs):
        """Testa obtenção de Pull Requests de repositório"""
        mock_prs = [
            GitHubPullRequest(
                id=1,
                number=1,
                title="Test PR",
                body="This is a test PR",
                state="open",
                locked=False,
                comments=0,
                review_comments=0,
                commits=1,
                additions=10,
                deletions=5,
                changed_files=2,
                author_association="NONE",
                labels=[],
                head={"ref": "feature-branch"},
                base={"ref": "main"},
                draft=False,
                merged=False,
                mergeable=None,
                mergeable_state="unknown",
                comments_url="https://api.github.com/repos/octocat/test-repo/issues/1/comments",
                review_comments_url="https://api.github.com/repos/octocat/test-repo/pulls/1/comments",
                commits_url="https://api.github.com/repos/octocat/test-repo/pulls/1/commits",
                statuses_url="https://api.github.com/repos/octocat/test-repo/statuses/abc123"
            )
        ]
        mock_get_prs.return_value = mock_prs
        
        response = client.get("/api/v1/repos/octocat/test-repo/pulls")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Test PR"
        assert data[0]["state"] == "open"


class TestSearchEndpoints:
    """Testes para endpoints de busca"""
    
    @patch('app.services.github_client.GitHubClient.search_repositories')
    def test_search_repositories_success(self, mock_search_repos):
        """Testa busca de repositórios"""
        mock_repos = [
            GitHubRepository(
                id=1,
                name="test-repo",
                full_name="octocat/test-repo",
                description="Test repository",
                private=False,
                fork=False,
                language="Python",
                size=100,
                stargazers_count=10,
                watchers_count=10,
                forks_count=5,
                open_issues_count=2,
                default_branch="main"
            )
        ]
        mock_search_repos.return_value = mock_repos
        
        response = client.get("/api/v1/search/repositories?q=python")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["language"] == "Python"
    
    @patch('app.services.github_client.GitHubClient.search_repositories')
    def test_search_repositories_with_pagination(self, mock_search_repos):
        """Testa busca de repositórios com paginação"""
        mock_search_repos.return_value = []
        
        response = client.get("/api/v1/search/repositories?q=python&page=2&per_page=20")
        assert response.status_code == 200
        mock_search_repos.assert_called_once_with("python", 2, 20)
    
    @patch('app.services.github_client.GitHubClient.search_users')
    def test_search_users_success(self, mock_search_users):
        """Testa busca de usuários"""
        mock_users = [
            GitHubUser(
                id=1,
                login="testuser",
                name="Test User",
                email=None,
                public_repos=5,
                public_gists=2,
                followers=10,
                following=5,
                type="User",
                site_admin=False
            )
        ]
        mock_search_users.return_value = mock_users
        
        response = client.get("/api/v1/search/users?q=testuser")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["login"] == "testuser"
    
    @patch('app.services.github_client.GitHubClient.search_users')
    def test_search_users_error(self, mock_search_users):
        """Testa erro na busca de usuários"""
        mock_search_users.side_effect = Exception("Search error")
        
        response = client.get("/api/v1/search/users?q=invalid")
        assert response.status_code == 400
        data = response.json()
        assert "Erro na busca" in data["detail"]


class TestErrorHandling:
    """Testes para tratamento de erros"""
    
    def test_invalid_endpoint(self):
        """Testa endpoint inexistente"""
        response = client.get("/api/v1/invalid")
        assert response.status_code == 404
    
    def test_invalid_query_parameters(self):
        """Testa parâmetros de query inválidos"""
        response = client.get("/api/v1/users/octocat/repositories?page=0")
        assert response.status_code == 422  # Validation error
    
    def test_missing_required_parameter(self):
        """Testa parâmetro obrigatório ausente"""
        response = client.get("/api/v1/search/repositories")
        assert response.status_code == 422  # Validation error


class TestIntegration:
    """Testes de integração"""
    
    @patch('app.services.github_client.GitHubClient.get_user')
    @patch('app.services.github_client.GitHubClient.get_user_repositories')
    def test_full_user_workflow(self, mock_get_repos, mock_get_user):
        """Testa workflow completo de usuário"""
        # Mock do usuário
        mock_user = GitHubUser(
            id=1,
            login="testuser",
            name="Test User",
            public_repos=2,
            public_gists=1,
            followers=5,
            following=3,
            type="User",
            site_admin=False
        )
        mock_get_user.return_value = mock_user
        
        # Mock dos repositórios
        mock_repos = [
            GitHubRepository(
                id=1,
                name="repo1",
                full_name="testuser/repo1",
                description="First repo",
                private=False,
                fork=False,
                language="Python",
                size=100,
                stargazers_count=5,
                watchers_count=5,
                forks_count=2,
                open_issues_count=1,
                default_branch="main"
            )
        ]
        mock_get_repos.return_value = mock_repos
        
        # Teste 1: Obter usuário
        response1 = client.get("/api/v1/users/testuser")
        assert response1.status_code == 200
        user_data = response1.json()
        assert user_data["login"] == "testuser"
        
        # Teste 2: Obter repositórios do usuário
        response2 = client.get("/api/v1/users/testuser/repositories")
        assert response2.status_code == 200
        repos_data = response2.json()
        assert len(repos_data) == 1
        assert repos_data[0]["name"] == "repo1"


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 