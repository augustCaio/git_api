"""
Testes automatizados completos para a GitHub Data API
"""

import pytest
from datetime import datetime
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
            ),
            GitHubRepository(
                id=2,
                name="test-repo-2",
                full_name="octocat/test-repo-2",
                description="Second test repository",
                private=True,
                fork=True,
                language="JavaScript",
                size=200,
                stargazers_count=5,
                watchers_count=5,
                forks_count=2,
                open_issues_count=1,
                default_branch="main"
            )
        ]
        mock_get_repos.return_value = mock_repos
        
        response = client.get("/api/v1/users/octocat/repositories")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["name"] == "test-repo"
        assert data[0]["language"] == "Python"
        assert data[0]["private"] == False
        assert data[1]["name"] == "test-repo-2"
        assert data[1]["language"] == "JavaScript"
        assert data[1]["private"] == True
        assert data[1]["fork"] == True
    
    @patch('app.services.github_client.GitHubClient.get_user_repositories')
    def test_get_user_repositories_with_max_per_page(self, mock_get_repos):
        """Testa obtenção de repositórios com máximo de itens por página"""
        mock_repos = [
            GitHubRepository(
                id=i,
                name=f"test-repo-{i}",
                full_name=f"octocat/test-repo-{i}",
                description=f"Test repository {i}",
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
            for i in range(1, 101)  # 100 repositórios
        ]
        mock_get_repos.return_value = mock_repos
        
        response = client.get("/api/v1/users/octocat/repositories?per_page=100")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 100
        mock_get_repos.assert_called_once_with("octocat", 1, 100)
    
    @patch('app.services.github_client.GitHubClient.get_user_repositories')
    def test_get_user_repositories_empty(self, mock_get_repos):
        """Testa obtenção de repositórios quando usuário não tem repositórios"""
        mock_get_repos.return_value = []
        
        response = client.get("/api/v1/users/emptyuser/repositories")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0
    
    @patch('app.services.github_client.GitHubClient.get_user_repositories')
    def test_get_user_repositories_all_types(self, mock_get_repos):
        """Testa obtenção de todos os tipos de repositórios (públicos, privados, forks)"""
        # Mock de repositórios com diferentes tipos
        mock_repos = [
            GitHubRepository(
                id=1,
                name="public-repo",
                full_name="octocat/public-repo",
                description="Public repository",
                private=False,
                fork=False,
                language="Python",
                size=100,
                stargazers_count=10,
                watchers_count=10,
                forks_count=5,
                open_issues_count=2,
                default_branch="main"
            ),
            GitHubRepository(
                id=2,
                name="private-repo",
                full_name="octocat/private-repo",
                description="Private repository",
                private=True,
                fork=False,
                language="JavaScript",
                size=200,
                stargazers_count=0,
                watchers_count=0,
                forks_count=0,
                open_issues_count=0,
                default_branch="main"
            ),
            GitHubRepository(
                id=3,
                name="forked-repo",
                full_name="octocat/forked-repo",
                description="Forked repository",
                private=False,
                fork=True,
                language="TypeScript",
                size=150,
                stargazers_count=5,
                watchers_count=5,
                forks_count=2,
                open_issues_count=1,
                default_branch="main"
            ),
            GitHubRepository(
                id=4,
                name="archived-repo",
                full_name="octocat/archived-repo",
                description="Archived repository",
                private=False,
                fork=False,
                language="HTML",
                size=50,
                stargazers_count=2,
                watchers_count=2,
                forks_count=1,
                open_issues_count=0,
                default_branch="main",
                archived=True
            )
        ]
        mock_get_repos.return_value = mock_repos
        
        response = client.get("/api/v1/users/octocat/repositories")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 4
        
        # Verifica se todos os tipos estão presentes
        repo_names = [repo["name"] for repo in data]
        assert "public-repo" in repo_names
        assert "private-repo" in repo_names
        assert "forked-repo" in repo_names
        assert "archived-repo" in repo_names
        
        # Verifica propriedades específicas
        public_repo = next(repo for repo in data if repo["name"] == "public-repo")
        private_repo = next(repo for repo in data if repo["name"] == "private-repo")
        forked_repo = next(repo for repo in data if repo["name"] == "forked-repo")
        archived_repo = next(repo for repo in data if repo["name"] == "archived-repo")
        
        assert public_repo["private"] == False
        assert public_repo["fork"] == False
        assert private_repo["private"] == True
        assert forked_repo["fork"] == True
        assert archived_repo.get("archived") == True
    
    @patch('app.services.github_client.GitHubClient.get_user_repositories')
    def test_get_user_repositories_with_pagination(self, mock_get_repos):
        """Testa paginação de repositórios"""
        mock_get_repos.return_value = []
        
        response = client.get("/api/v1/users/octocat/repositories?page=2&per_page=10")
        assert response.status_code == 200
        mock_get_repos.assert_called_once_with("octocat", 2, 10)
    
    @patch('app.services.github_client.GitHubClient.get_user_repositories')
    def test_get_user_repositories_summary_success(self, mock_get_repos):
        """Testa obtenção de resumo de repositórios com sucesso"""
        # Mock dos repositórios
        mock_repos = [
            GitHubRepository(
                id=1,
                name="test-repo-1",
                full_name="octocat/test-repo-1",
                description="First test repository",
                private=False,
                fork=False,
                language="Python",
                size=100,
                stargazers_count=10,
                watchers_count=10,
                forks_count=5,
                open_issues_count=2,
                default_branch="main",
                created_at=datetime.fromisoformat("2025-01-01T10:00:00+00:00"),
                updated_at=datetime.fromisoformat("2025-07-29T16:00:00+00:00")
            ),
            GitHubRepository(
                id=2,
                name="test-repo-2",
                full_name="octocat/test-repo-2",
                description="Second test repository",
                private=True,
                fork=True,
                language="JavaScript",
                size=200,
                stargazers_count=5,
                watchers_count=5,
                forks_count=2,
                open_issues_count=1,
                default_branch="main",
                created_at=datetime.fromisoformat("2025-01-02T10:00:00+00:00"),
                updated_at=datetime.fromisoformat("2025-07-28T15:00:00+00:00")
            ),
            GitHubRepository(
                id=3,
                name="test-repo-3",
                full_name="octocat/test-repo-3",
                description="Third test repository",
                private=False,
                fork=False,
                language="Python",
                size=150,
                stargazers_count=15,
                watchers_count=15,
                forks_count=8,
                open_issues_count=3,
                default_branch="main",
                created_at=datetime.fromisoformat("2025-01-03T10:00:00+00:00"),
                updated_at=datetime.fromisoformat("2025-07-27T14:00:00+00:00")
            )
        ]
        mock_get_repos.return_value = mock_repos
        
        response = client.get("/api/v1/users/octocat/repositories/summary")
        assert response.status_code == 200
        data = response.json()
        
        # Verifica estrutura básica
        assert data["username"] == "octocat"
        assert "summary" in data
        assert "languages" in data
        assert "top_repositories" in data
        assert "recent_activity" in data
        
        # Verifica estatísticas
        summary = data["summary"]
        assert summary["total_repositories"] == 3
        assert summary["public_repositories"] == 2
        assert summary["private_repositories"] == 1
        assert summary["total_stars"] == 30  # 10 + 5 + 15
        assert summary["total_forks"] == 15  # 5 + 2 + 8
        assert summary["total_watchers"] == 30  # 10 + 5 + 15
        assert summary["total_size"] == 450  # 100 + 200 + 150
        
        # Verifica linguagens
        languages = data["languages"]
        assert "Python" in languages
        assert "JavaScript" in languages
        assert languages["Python"]["count"] == 2
        assert abs(languages["Python"]["percentage"] - 66.66666666666667) < 0.01  # Tolerância para ponto flutuante
        assert languages["JavaScript"]["count"] == 1
        assert abs(languages["JavaScript"]["percentage"] - 33.33333333333333) < 0.01  # Tolerância para ponto flutuante
        
        # Verifica top repositórios (ordenados por stars)
        top_repos = data["top_repositories"]
        assert len(top_repos) == 3
        assert top_repos[0]["name"] == "test-repo-3"  # 15 stars
        assert top_repos[0]["stars"] == 15
        assert top_repos[1]["name"] == "test-repo-1"  # 10 stars
        assert top_repos[1]["stars"] == 10
        assert top_repos[2]["name"] == "test-repo-2"  # 5 stars
        assert top_repos[2]["stars"] == 5
        
        # Verifica atividade recente (ordenados por updated_at)
        recent_activity = data["recent_activity"]
        assert len(recent_activity) == 3
        assert recent_activity[0]["name"] == "test-repo-1"  # mais recente
        assert recent_activity[1]["name"] == "test-repo-2"
        assert recent_activity[2]["name"] == "test-repo-3"  # mais antigo
    
    @patch('app.services.github_client.GitHubClient.get_user_repositories')
    def test_get_user_repositories_summary_empty(self, mock_get_repos):
        """Testa resumo de repositórios quando usuário não tem repositórios"""
        mock_get_repos.return_value = []
        
        response = client.get("/api/v1/users/emptyuser/repositories/summary")
        assert response.status_code == 200
        data = response.json()
        
        assert data["username"] == "emptyuser"
        summary = data["summary"]
        assert summary["total_repositories"] == 0
        assert summary["public_repositories"] == 0
        assert summary["private_repositories"] == 0
        assert summary["total_stars"] == 0
        assert summary["total_forks"] == 0
        assert summary["total_watchers"] == 0
        assert summary["total_size"] == 0
        assert data["languages"] == {}
        assert data["top_repositories"] == []
        assert data["recent_activity"] == []
    
    @patch('app.services.github_client.GitHubClient.get_user_repositories')
    def test_get_user_repositories_summary_error(self, mock_get_repos):
        """Testa erro ao buscar resumo de repositórios"""
        mock_get_repos.side_effect = Exception("API Error")
        
        response = client.get("/api/v1/users/erroruser/repositories/summary")
        assert response.status_code == 404
        data = response.json()
        assert "Erro ao buscar resumo dos repositórios" in data["detail"]
    
    @patch('app.services.github_client.GitHubClient.get_user_repositories')
    def test_get_user_repositories_summary_without_language(self, mock_get_repos):
        """Testa resumo de repositórios com repositórios sem linguagem definida"""
        mock_repos = [
            GitHubRepository(
                id=1,
                name="repo-with-language",
                full_name="octocat/repo-with-language",
                description="Repository with language",
                private=False,
                fork=False,
                language="Python",
                size=100,
                stargazers_count=10,
                watchers_count=10,
                forks_count=5,
                open_issues_count=2,
                default_branch="main"
            ),
            GitHubRepository(
                id=2,
                name="repo-without-language",
                full_name="octocat/repo-without-language",
                description="Repository without language",
                private=False,
                fork=False,
                language=None,  # Sem linguagem definida
                size=200,
                stargazers_count=5,
                watchers_count=5,
                forks_count=2,
                open_issues_count=1,
                default_branch="main"
            )
        ]
        mock_get_repos.return_value = mock_repos
        
        response = client.get("/api/v1/users/octocat/repositories/summary")
        assert response.status_code == 200
        data = response.json()
        
        # Verifica que apenas Python está nas linguagens (repo sem linguagem é ignorado)
        languages = data["languages"]
        assert "Python" in languages
        assert len(languages) == 1
        assert languages["Python"]["count"] == 1
        assert abs(languages["Python"]["percentage"] - 50.0) < 0.01  # Tolerância para ponto flutuante
        
        # Verifica que ambos os repositórios estão nas listas
        top_repos = data["top_repositories"]
        assert len(top_repos) == 2
        repo_names = [repo["name"] for repo in top_repos]
        assert "repo-with-language" in repo_names
        assert "repo-without-language" in repo_names

    @patch('app.services.github_client.GitHubClient.get_user_languages')
    def test_get_user_languages_success(self, mock_get_languages):
        """Testa obtenção de linguagens do usuário com sucesso"""
        mock_languages = {
            "Python": {"count": 5, "percentage": 50.0},
            "JavaScript": {"count": 3, "percentage": 30.0},
            "TypeScript": {"count": 2, "percentage": 20.0}
        }
        mock_get_languages.return_value = mock_languages
        
        response = client.get("/api/v1/users/octocat/languages")
        assert response.status_code == 200
        data = response.json()
        
        assert data["username"] == "octocat"
        assert data["total_languages"] == 3
        assert "Python" in data["languages"]
        assert data["languages"]["Python"]["count"] == 5
        assert data["languages"]["Python"]["percentage"] == 50.0
        assert "JavaScript" in data["languages"]
        assert "TypeScript" in data["languages"]

    @patch('app.services.github_client.GitHubClient.get_user_languages')
    def test_get_user_languages_error(self, mock_get_languages):
        """Testa erro ao buscar linguagens do usuário"""
        mock_get_languages.side_effect = Exception("API Error")
        
        response = client.get("/api/v1/users/erroruser/languages")
        assert response.status_code == 404
        data = response.json()
        assert "Erro ao buscar linguagens" in data["detail"]

    @patch('app.services.github_client.GitHubClient.get_user_stats')
    def test_get_user_stats_success(self, mock_get_stats):
        """Testa obtenção de estatísticas do usuário com sucesso"""
        mock_stats = {
            "user": {
                "id": 583231,
                "login": "octocat",
                "name": "The Octocat",
                "public_repos": 8,
                "followers": 1000,
                "following": 9
            },
            "repositories": {
                "total": 8,
                "public": 6,
                "private": 2,
                "total_stars": 150,
                "total_forks": 25
            },
            "activity": {
                "last_commit": "2025-07-29T16:00:00Z",
                "recent_commits": 15,
                "recent_issues": 3
            },
            "languages": {
                "Python": {"count": 3, "percentage": 37.5},
                "JavaScript": {"count": 2, "percentage": 25.0}
            },
            "top_repositories": [
                {
                    "name": "best-repo",
                    "stars": 50,
                    "forks": 10,
                    "language": "Python"
                }
            ]
        }
        mock_get_stats.return_value = mock_stats
        
        response = client.get("/api/v1/users/octocat/stats")
        assert response.status_code == 200
        data = response.json()
        
        assert data["username"] == "octocat"
        assert data["user"]["login"] == "octocat"
        assert data["user"]["id"] == 583231
        assert data["repositories"]["total"] == 8
        assert data["repositories"]["total_stars"] == 150
        assert "Python" in data["languages"]
        assert len(data["top_repositories"]) == 1
        assert data["top_repositories"][0]["name"] == "best-repo"

    @patch('app.services.github_client.GitHubClient.get_user_stats')
    def test_get_user_stats_error(self, mock_get_stats):
        """Testa erro ao buscar estatísticas do usuário"""
        mock_get_stats.side_effect = Exception("API Error")
        
        response = client.get("/api/v1/users/erroruser/stats")
        assert response.status_code == 404
        data = response.json()
        assert "Erro ao buscar estatísticas" in data["detail"]


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


class TestCacheEndpoints:
    """Testes para endpoints de cache"""
    
    @patch('app.services.cache_service.cache_service.get_stats')
    def test_cache_stats_success(self, mock_get_stats):
        """Testa obtenção de estatísticas do cache"""
        mock_stats = {
            "memory_cache_size": 5,
            "memory_cache_maxsize": 1000,
            "use_redis": False,
            "redis_connected": False
        }
        mock_get_stats.return_value = mock_stats
        
        response = client.get("/api/v1/cache/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["memory_cache_size"] == 5
        assert data["memory_cache_maxsize"] == 1000
        assert data["use_redis"] == False
        assert data["redis_connected"] == False

    @patch('app.services.cache_service.cache_service.clear')
    def test_clear_cache_success(self, mock_clear):
        """Testa limpeza do cache com sucesso"""
        mock_clear.return_value = True
        
        response = client.delete("/api/v1/cache/clear")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "Cache limpo com sucesso" in data["message"]

    @patch('app.services.cache_service.cache_service.clear')
    def test_clear_cache_error(self, mock_clear):
        """Testa erro ao limpar cache"""
        mock_clear.return_value = False
        
        response = client.delete("/api/v1/cache/clear")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == False
        assert "Erro ao limpar cache" in data["message"]


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