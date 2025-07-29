"""
Testes para os novos endpoints da Semana 2
"""

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.models.github_models import GitHubUser, GitHubRepository, GitHubLanguage

client = TestClient(app)


class TestUserLanguagesEndpoint:
    """Testes para o endpoint /users/{username}/languages"""
    
    @patch('app.services.github_client.GitHubClient.get_user_languages')
    def test_get_user_languages_success(self, mock_get_languages):
        """Testa busca bem-sucedida de linguagens do usuário"""
        # Mock das linguagens
        mock_languages = {
            "Python": GitHubLanguage(name="Python", bytes=1000, percentage=50.0),
            "JavaScript": GitHubLanguage(name="JavaScript", bytes=500, percentage=25.0),
            "TypeScript": GitHubLanguage(name="TypeScript", bytes=500, percentage=25.0)
        }
        mock_get_languages.return_value = mock_languages
        
        response = client.get("/api/v1/users/octocat/languages")
        assert response.status_code == 200
        
        data = response.json()
        assert data["username"] == "octocat"
        assert len(data["languages"]) == 3
        assert data["total_languages"] == 3
        assert "Python" in data["languages"]
        assert "JavaScript" in data["languages"]
        assert "TypeScript" in data["languages"]
    
    @patch('app.services.github_client.GitHubClient.get_user_languages')
    def test_get_user_languages_not_found(self, mock_get_languages):
        """Testa usuário não encontrado"""
        mock_get_languages.side_effect = Exception("User not found")
        
        response = client.get("/api/v1/users/nonexistent/languages")
        assert response.status_code == 404
        assert "Erro ao buscar linguagens" in response.json()["detail"]


class TestUserStatsEndpoint:
    """Testes para o endpoint /users/{username}/stats"""
    
    @patch('app.services.github_client.GitHubClient.get_user_stats')
    def test_get_user_stats_success(self, mock_get_stats):
        """Testa busca bem-sucedida de estatísticas do usuário"""
        # Mock das estatísticas
        mock_user = GitHubUser(
            id=1,
            login="octocat",
            name="The Octocat",
            public_repos=10,
            followers=100,
            following=50
        )
        
        mock_stats = {
            "user": mock_user,
            "repositories": {
                "total": 10,
                "public": 8,
                "private": 2,
                "forked": 3,
                "original": 7
            },
            "activity": {
                "total_stars": 500,
                "total_forks": 100,
                "total_issues": 25,
                "average_stars_per_repo": 50.0
            },
            "languages": {
                "top_languages": [
                    {"language": "Python", "count": 5},
                    {"language": "JavaScript", "count": 3}
                ],
                "total_languages": 2
            },
            "top_repositories": [
                {
                    "name": "repo1",
                    "full_name": "octocat/repo1",
                    "description": "First repo",
                    "stars": 100,
                    "forks": 20,
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
        assert data["repositories"]["total"] == 10
        assert data["activity"]["total_stars"] == 500
        assert len(data["languages"]["top_languages"]) == 2
        assert len(data["top_repositories"]) == 1
    
    @patch('app.services.github_client.GitHubClient.get_user_stats')
    def test_get_user_stats_not_found(self, mock_get_stats):
        """Testa usuário não encontrado"""
        mock_get_stats.side_effect = Exception("User not found")
        
        response = client.get("/api/v1/users/nonexistent/stats")
        assert response.status_code == 404
        assert "Erro ao buscar estatísticas" in response.json()["detail"]


class TestEnhancedUserEndpoints:
    """Testes para endpoints de usuário melhorados"""
    
    @patch('app.services.github_client.GitHubClient.get_user')
    def test_get_user_enhanced(self, mock_get_user):
        """Testa endpoint de usuário com resposta melhorada"""
        mock_user = GitHubUser(
            id=1,
            login="octocat",
            name="The Octocat",
            email="octocat@github.com",
            avatar_url="https://avatars.githubusercontent.com/u/583231?v=4",
            bio="GitHub mascot",
            location="San Francisco",
            company="@github",
            public_repos=10,
            public_gists=5,
            followers=100,
            following=50,
            type="User",
            site_admin=False
        )
        mock_get_user.return_value = mock_user
        
        response = client.get("/api/v1/users/octocat")
        assert response.status_code == 200
        
        data = response.json()
        assert data["login"] == "octocat"
        assert data["name"] == "The Octocat"
        assert data["public_repos"] == 10
        assert data["followers"] == 100
        assert data["following"] == 50
    
    @patch('app.services.github_client.GitHubClient.get_user_repositories')
    def test_get_user_repositories_enhanced(self, mock_get_repos):
        """Testa endpoint de repositórios com paginação"""
        mock_repos = [
            GitHubRepository(
                id=1,
                name="repo1",
                full_name="octocat/repo1",
                description="First repository",
                private=False,
                fork=False,
                language="Python",
                size=100,
                stargazers_count=50,
                watchers_count=50,
                forks_count=10,
                open_issues_count=5,
                default_branch="main"
            ),
            GitHubRepository(
                id=2,
                name="repo2",
                full_name="octocat/repo2",
                description="Second repository",
                private=False,
                fork=True,
                language="JavaScript",
                size=200,
                stargazers_count=25,
                watchers_count=25,
                forks_count=5,
                open_issues_count=2,
                default_branch="main"
            )
        ]
        mock_get_repos.return_value = mock_repos
        
        response = client.get("/api/v1/users/octocat/repositories?page=1&per_page=10")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 2
        assert data[0]["name"] == "repo1"
        assert data[0]["language"] == "Python"
        assert data[1]["name"] == "repo2"
        assert data[1]["language"] == "JavaScript"


class TestErrorHandling:
    """Testes para tratamento de erros nos novos endpoints"""
    
    def test_invalid_username_format(self):
        """Testa formato de username inválido"""
        response = client.get("/api/v1/users/invalid@user/languages")
        assert response.status_code == 404
    
    def test_missing_username(self):
        """Testa username ausente"""
        response = client.get("/api/v1/users//languages")
        assert response.status_code == 404
    
    @patch('app.services.github_client.GitHubClient.get_user_languages')
    def test_api_rate_limit_error(self, mock_get_languages):
        """Testa erro de rate limit da API do GitHub"""
        mock_get_languages.side_effect = Exception("API rate limit exceeded")
        
        response = client.get("/api/v1/users/octocat/languages")
        assert response.status_code == 404
        assert "Erro ao buscar linguagens" in response.json()["detail"]


class TestIntegration:
    """Testes de integração para os novos endpoints"""
    
    @patch('app.services.github_client.GitHubClient.get_user_stats')
    @patch('app.services.github_client.GitHubClient.get_user_languages')
    def test_user_complete_workflow(self, mock_get_languages, mock_get_stats):
        """Testa workflow completo de usuário com novos endpoints"""
        # Mock para linguagens
        mock_languages = {
            "Python": GitHubLanguage(name="Python", bytes=1000, percentage=60.0),
            "JavaScript": GitHubLanguage(name="JavaScript", bytes=400, percentage=40.0)
        }
        mock_get_languages.return_value = mock_languages
        
        # Mock para estatísticas
        mock_user = GitHubUser(
            id=1,
            login="testuser",
            name="Test User",
            public_repos=5,
            followers=50,
            following=25
        )
        
        mock_stats = {
            "user": mock_user,
            "repositories": {"total": 5, "public": 4, "private": 1, "forked": 1, "original": 4},
            "activity": {"total_stars": 200, "total_forks": 30, "total_issues": 10, "average_stars_per_repo": 40.0},
            "languages": {"top_languages": [{"language": "Python", "count": 3}], "total_languages": 1},
            "top_repositories": [{"name": "test-repo", "full_name": "testuser/test-repo", "stars": 50}]
        }
        mock_get_stats.return_value = mock_stats
        
        # Teste 1: Linguagens do usuário
        response1 = client.get("/api/v1/users/testuser/languages")
        assert response1.status_code == 200
        data1 = response1.json()
        assert data1["username"] == "testuser"
        assert data1["total_languages"] == 2
        
        # Teste 2: Estatísticas do usuário
        response2 = client.get("/api/v1/users/testuser/stats")
        assert response2.status_code == 200
        data2 = response2.json()
        assert data2["username"] == "testuser"
        assert data2["repositories"]["total"] == 5
        assert data2["activity"]["total_stars"] == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 