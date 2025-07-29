"""
Configuração global do pytest para testes da GitHub Data API
"""

import pytest
from unittest.mock import MagicMock
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
def sample_user():
    """Fixture para usuário de exemplo"""
    return GitHubUser(
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


@pytest.fixture
def sample_repository():
    """Fixture para repositório de exemplo"""
    return GitHubRepository(
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


@pytest.fixture
def sample_languages():
    """Fixture para linguagens de exemplo"""
    return {
        "Python": GitHubLanguage(name="Python", bytes=1000, percentage=60.0),
        "JavaScript": GitHubLanguage(name="JavaScript", bytes=400, percentage=24.0),
        "HTML": GitHubLanguage(name="HTML", bytes=300, percentage=16.0)
    }


@pytest.fixture
def sample_event():
    """Fixture para evento de exemplo"""
    return GitHubEvent(
        id="123",
        type="PushEvent",
        public=True,
        repo={"id": 1, "name": "octocat/test-repo"},
        payload={"ref": "main", "commits": []}
    )


@pytest.fixture
def sample_commit():
    """Fixture para commit de exemplo"""
    return GitHubCommit(
        sha="abc123",
        node_id="MDY6Q29tbWl0MTIz",
        commit={"message": "Initial commit"},
        url="https://api.github.com/repos/octocat/test-repo/commits/abc123",
        html_url="https://github.com/octocat/test-repo/commit/abc123",
        comments_url="https://api.github.com/repos/octocat/test-repo/commits/abc123/comments"
    )


@pytest.fixture
def sample_issue():
    """Fixture para issue de exemplo"""
    return GitHubIssue(
        id=1,
        number=1,
        title="Test Issue",
        body="This is a test issue",
        state="open",
        locked=False,
        comments=5,
        author_association="NONE",
        labels=[
            {"id": 1, "name": "bug", "color": "d73a4a"},
            {"id": 2, "name": "help wanted", "color": "008672"}
        ]
    )


@pytest.fixture
def sample_pull_request():
    """Fixture para Pull Request de exemplo"""
    return GitHubPullRequest(
        id=1,
        number=1,
        title="Test PR",
        body="This is a test PR",
        state="open",
        locked=False,
        comments=3,
        review_comments=2,
        commits=5,
        additions=100,
        deletions=50,
        changed_files=10,
        author_association="NONE",
        labels=[],
        head={"ref": "feature-branch", "sha": "abc123"},
        base={"ref": "main", "sha": "def456"},
        draft=False,
        merged=False,
        mergeable=None,
        mergeable_state="unknown",
        comments_url="https://api.github.com/repos/octocat/test-repo/issues/1/comments",
        review_comments_url="https://api.github.com/repos/octocat/test-repo/pulls/1/comments",
        commits_url="https://api.github.com/repos/octocat/test-repo/pulls/1/commits",
        statuses_url="https://api.github.com/repos/octocat/test-repo/statuses/abc123"
    )


@pytest.fixture
def mock_github_client():
    """Fixture para mock do cliente GitHub"""
    mock_client = MagicMock()
    
    # Mock dos métodos do cliente
    mock_client.get_user.return_value = sample_user()
    mock_client.get_user_repositories.return_value = [sample_repository()]
    mock_client.get_repository.return_value = sample_repository()
    mock_client.get_repository_languages.return_value = sample_languages()
    mock_client.get_repository_events.return_value = [sample_event()]
    mock_client.get_repository_commits.return_value = [sample_commit()]
    mock_client.get_repository_issues.return_value = [sample_issue()]
    mock_client.get_repository_pull_requests.return_value = [sample_pull_request()]
    mock_client.search_repositories.return_value = [sample_repository()]
    mock_client.search_users.return_value = [sample_user()]
    
    return mock_client


@pytest.fixture
def mock_http_response():
    """Fixture para mock de resposta HTTP"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
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
    return mock_response


# Configurações globais do pytest
def pytest_configure(config):
    """Configuração do pytest"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )


def pytest_collection_modifyitems(config, items):
    """Modifica itens de teste durante a coleta"""
    for item in items:
        # Marca testes de API como integration
        if "test_api" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        # Marca testes de cliente como unit
        elif "test_github_client" in item.nodeid:
            item.add_marker(pytest.mark.unit)
        # Marca testes de modelos como unit
        elif "test_models" in item.nodeid:
            item.add_marker(pytest.mark.unit) 