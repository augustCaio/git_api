"""
Testes para os modelos Pydantic
"""

import pytest
from datetime import datetime
from pydantic import ValidationError
from app.models.github_models import (
    GitHubUser,
    GitHubRepository,
    GitHubLanguage,
    GitHubEvent,
    GitHubCommit,
    GitHubIssue,
    GitHubPullRequest,
)


class TestGitHubUser:
    """Testes para o modelo GitHubUser"""
    
    def test_github_user_valid_data(self):
        """Testa criação de usuário com dados válidos"""
        user_data = {
            "id": 583231,
            "login": "octocat",
            "name": "The Octocat",
            "email": None,
            "avatar_url": "https://avatars.githubusercontent.com/u/583231?v=4",
            "bio": None,
            "location": "San Francisco",
            "company": "@github",
            "blog": "https://github.blog",
            "twitter_username": "octocat",
            "public_repos": 8,
            "public_gists": 8,
            "followers": 1000,
            "following": 9,
            "created_at": "2011-01-25T18:44:36Z",
            "updated_at": "2023-01-25T18:44:36Z",
            "hireable": True,
            "type": "User",
            "site_admin": False
        }
        
        user = GitHubUser(**user_data)
        
        assert user.id == 583231
        assert user.login == "octocat"
        assert user.name == "The Octocat"
        assert user.email is None
        assert str(user.avatar_url) == "https://avatars.githubusercontent.com/u/583231?v=4"
        assert user.location == "San Francisco"
        assert user.company == "@github"
        assert str(user.blog) == "https://github.blog/"
        assert user.public_repos == 8
        assert user.followers == 1000
        assert user.type == "User"
        assert user.site_admin is False
    
    def test_github_user_minimal_data(self):
        """Testa criação de usuário com dados mínimos"""
        user_data = {
            "id": 1,
            "login": "testuser"
        }
        
        user = GitHubUser(**user_data)
        
        assert user.id == 1
        assert user.login == "testuser"
        assert user.name is None
        assert user.email is None
        assert user.public_repos == 0
        assert user.followers == 0
        assert user.type == "User"
        assert user.site_admin is False
    
    def test_github_user_invalid_data(self):
        """Testa criação de usuário com dados inválidos"""
        user_data = {
            "id": "invalid_id",  # ID deve ser int
            "login": 123  # login deve ser str
        }
        
        with pytest.raises(ValidationError):
            GitHubUser(**user_data)


class TestGitHubRepository:
    """Testes para o modelo GitHubRepository"""
    
    def test_github_repository_valid_data(self):
        """Testa criação de repositório com dados válidos"""
        repo_data = {
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
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-02T00:00:00Z",
            "pushed_at": "2023-01-03T00:00:00Z",
            "homepage": "https://github.com/octocat/test-repo",
            "topics": ["test", "python"],
            "archived": False,
            "disabled": False,
            "license": {
                "key": "mit",
                "name": "MIT License",
                "url": "https://api.github.com/licenses/mit"
            }
        }
        
        repo = GitHubRepository(**repo_data)
        
        assert repo.id == 1
        assert repo.name == "test-repo"
        assert repo.full_name == "octocat/test-repo"
        assert repo.description == "Test repository"
        assert repo.private is False
        assert repo.fork is False
        assert repo.language == "Python"
        assert repo.size == 100
        assert repo.stargazers_count == 10
        assert repo.forks_count == 5
        assert repo.default_branch == "main"
        assert repo.topics == ["test", "python"]
        assert str(repo.homepage) == "https://github.com/octocat/test-repo"
        assert repo.archived is False
        assert repo.disabled is False
        assert repo.license is not None and repo.license["key"] == "mit"
    
    def test_github_repository_minimal_data(self):
        """Testa criação de repositório com dados mínimos"""
        repo_data = {
            "id": 1,
            "name": "test-repo",
            "full_name": "octocat/test-repo"
        }
        
        repo = GitHubRepository(**repo_data)
        
        assert repo.id == 1
        assert repo.name == "test-repo"
        assert repo.full_name == "octocat/test-repo"
        assert repo.description is None
        assert repo.private is False
        assert repo.fork is False
        assert repo.language is None
        assert repo.size == 0
        assert repo.stargazers_count == 0
        assert repo.default_branch == "main"
        assert repo.topics == []
        assert repo.archived is False
        assert repo.disabled is False


class TestGitHubLanguage:
    """Testes para o modelo GitHubLanguage"""
    
    def test_github_language_valid_data(self):
        """Testa criação de linguagem com dados válidos"""
        language_data = {
            "name": "Python",
            "bytes": 1000,
            "percentage": 60.0
        }
        
        language = GitHubLanguage(**language_data)
        
        assert language.name == "Python"
        assert language.bytes == 1000
        assert language.percentage == 60.0
    
    def test_github_language_minimal_data(self):
        """Testa criação de linguagem com dados mínimos"""
        language_data = {
            "name": "Python",
            "bytes": 1000
        }
        
        language = GitHubLanguage(**language_data)
        
        assert language.name == "Python"
        assert language.bytes == 1000
        assert language.percentage == 0.0


class TestGitHubEvent:
    """Testes para o modelo GitHubEvent"""
    
    def test_github_event_valid_data(self):
        """Testa criação de evento com dados válidos"""
        event_data = {
            "id": "123",
            "type": "PushEvent",
            "public": True,
            "created_at": "2023-01-01T00:00:00Z",
            "repo": {"id": 1, "name": "octocat/test-repo"},
            "payload": {"ref": "main", "commits": []}
        }
        
        event = GitHubEvent(**event_data)
        
        assert event.id == "123"
        assert event.type == "PushEvent"
        assert event.public is True
        assert event.repo == {"id": 1, "name": "octocat/test-repo"}
        assert event.payload == {"ref": "main", "commits": []}
    
    def test_github_event_minimal_data(self):
        """Testa criação de evento com dados mínimos"""
        event_data = {
            "id": "123",
            "type": "PushEvent"
        }
        
        event = GitHubEvent(**event_data)
        
        assert event.id == "123"
        assert event.type == "PushEvent"
        assert event.public is True
        assert event.repo is None
        assert event.payload is None


class TestGitHubCommit:
    """Testes para o modelo GitHubCommit"""
    
    def test_github_commit_valid_data(self):
        """Testa criação de commit com dados válidos"""
        commit_data = {
            "sha": "abc123",
            "node_id": "MDY6Q29tbWl0MTIz",
            "commit": {
                "message": "Initial commit",
                "author": {"name": "Test Author", "email": "test@example.com"},
                "committer": {"name": "Test Committer", "email": "test@example.com"}
            },
            "url": "https://api.github.com/repos/octocat/test-repo/commits/abc123",
            "html_url": "https://github.com/octocat/test-repo/commit/abc123",
            "comments_url": "https://api.github.com/repos/octocat/test-repo/commits/abc123/comments",
            "parents": [{"sha": "def456", "url": "https://api.github.com/repos/octocat/test-repo/commits/def456"}]
        }
        
        commit = GitHubCommit(**commit_data)
        
        assert commit.sha == "abc123"
        assert commit.node_id == "MDY6Q29tbWl0MTIz"
        assert commit.commit["message"] == "Initial commit"
        assert str(commit.url) == "https://api.github.com/repos/octocat/test-repo/commits/abc123"
        assert str(commit.html_url) == "https://github.com/octocat/test-repo/commit/abc123"
        assert len(commit.parents) == 1
        assert commit.parents[0]["sha"] == "def456"


class TestGitHubIssue:
    """Testes para o modelo GitHubIssue"""
    
    def test_github_issue_valid_data(self):
        """Testa criação de issue com dados válidos"""
        issue_data = {
            "id": 1,
            "number": 1,
            "title": "Test Issue",
            "body": "This is a test issue",
            "state": "open",
            "locked": False,
            "comments": 5,
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-02T00:00:00Z",
            "closed_at": None,
            "author_association": "NONE",
            "labels": [
                {"id": 1, "name": "bug", "color": "d73a4a"},
                {"id": 2, "name": "help wanted", "color": "008672"}
            ]
        }
        
        issue = GitHubIssue(**issue_data)
        
        assert issue.id == 1
        assert issue.number == 1
        assert issue.title == "Test Issue"
        assert issue.body == "This is a test issue"
        assert issue.state == "open"
        assert issue.locked is False
        assert issue.comments == 5
        assert issue.author_association == "NONE"
        assert len(issue.labels) == 2
        assert issue.labels[0]["name"] == "bug"
        assert issue.labels[1]["name"] == "help wanted"


class TestGitHubPullRequest:
    """Testes para o modelo GitHubPullRequest"""
    
    def test_github_pull_request_valid_data(self):
        """Testa criação de Pull Request com dados válidos"""
        pr_data = {
            "id": 1,
            "number": 1,
            "title": "Test PR",
            "body": "This is a test PR",
            "state": "open",
            "locked": False,
            "comments": 3,
            "review_comments": 2,
            "commits": 5,
            "additions": 100,
            "deletions": 50,
            "changed_files": 10,
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-02T00:00:00Z",
            "closed_at": None,
            "merged_at": None,
            "merge_commit_sha": None,
            "author_association": "NONE",
            "labels": [],
            "head": {"ref": "feature-branch", "sha": "abc123"},
            "base": {"ref": "main", "sha": "def456"},
            "draft": False,
            "merged": False,
            "mergeable": None,
            "mergeable_state": "unknown",
            "comments_url": "https://api.github.com/repos/octocat/test-repo/issues/1/comments",
            "review_comments_url": "https://api.github.com/repos/octocat/test-repo/pulls/1/comments",
            "commits_url": "https://api.github.com/repos/octocat/test-repo/pulls/1/commits",
            "statuses_url": "https://api.github.com/repos/octocat/test-repo/statuses/abc123"
        }
        
        pr = GitHubPullRequest(**pr_data)
        
        assert pr.id == 1
        assert pr.number == 1
        assert pr.title == "Test PR"
        assert pr.body == "This is a test PR"
        assert pr.state == "open"
        assert pr.locked is False
        assert pr.comments == 3
        assert pr.review_comments == 2
        assert pr.commits == 5
        assert pr.additions == 100
        assert pr.deletions == 50
        assert pr.changed_files == 10
        assert pr.draft is False
        assert pr.merged is False
        assert str(pr.comments_url) == "https://api.github.com/repos/octocat/test-repo/issues/1/comments"
        assert str(pr.review_comments_url) == "https://api.github.com/repos/octocat/test-repo/pulls/1/comments"
        assert str(pr.commits_url) == "https://api.github.com/repos/octocat/test-repo/pulls/1/commits"
        assert str(pr.statuses_url) == "https://api.github.com/repos/octocat/test-repo/statuses/abc123"
        assert pr.head["ref"] == "feature-branch"
        assert pr.base["ref"] == "main"


class TestModelValidation:
    """Testes de validação de modelos"""
    
    def test_github_user_url_validation(self):
        """Testa validação de URLs no modelo GitHubUser"""
        user_data = {
            "id": 1,
            "login": "testuser",
            "avatar_url": "invalid-url"  # URL inválida
        }
        
        with pytest.raises(ValidationError):
            GitHubUser(**user_data)
    
    def test_github_repository_url_validation(self):
        """Testa validação de URLs no modelo GitHubRepository"""
        # Testa com URL válida (homepage agora aceita qualquer string)
        repo_data = {
            "id": 1,
            "name": "test-repo",
            "full_name": "octocat/test-repo",
            "homepage": "https://example.com"  # URL válida
        }
        
        repo = GitHubRepository(**repo_data)
        assert repo.homepage == "https://example.com"
        
        # Testa com string inválida (deve aceitar)
        repo_data_invalid = {
            "id": 1,
            "name": "test-repo",
            "full_name": "octocat/test-repo",
            "homepage": "invalid-url"  # String inválida, mas aceita
        }
        
        repo_invalid = GitHubRepository(**repo_data_invalid)
        assert repo_invalid.homepage == "invalid-url"
    
    def test_github_commit_url_validation(self):
        """Testa validação de URLs no modelo GitHubCommit"""
        commit_data = {
            "sha": "abc123",
            "node_id": "MDY6Q29tbWl0MTIz",
            "commit": {"message": "Initial commit"},
            "url": "invalid-url",  # URL inválida
            "html_url": "https://github.com/octocat/test-repo/commit/abc123",
            "comments_url": "https://api.github.com/repos/octocat/test-repo/commits/abc123/comments"
        }
        
        with pytest.raises(ValidationError):
            GitHubCommit(**commit_data)


class TestModelSerialization:
    """Testes de serialização de modelos"""
    
    def test_github_user_serialization(self):
        """Testa serialização do modelo GitHubUser"""
        user = GitHubUser(
            id=1,
            login="testuser",
            name="Test User",
            public_repos=5,
            followers=10
        )
        
        user_dict = user.model_dump()
        
        assert user_dict["id"] == 1
        assert user_dict["login"] == "testuser"
        assert user_dict["name"] == "Test User"
        assert user_dict["public_repos"] == 5
        assert user_dict["followers"] == 10
    
    def test_github_repository_serialization(self):
        """Testa serialização do modelo GitHubRepository"""
        repo = GitHubRepository(
            id=1,
            name="test-repo",
            full_name="octocat/test-repo",
            description="Test repository",
            language="Python",
            stargazers_count=10
        )
        
        repo_dict = repo.model_dump()
        
        assert repo_dict["id"] == 1
        assert repo_dict["name"] == "test-repo"
        assert repo_dict["full_name"] == "octocat/test-repo"
        assert repo_dict["description"] == "Test repository"
        assert repo_dict["language"] == "Python"
        assert repo_dict["stargazers_count"] == 10


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 