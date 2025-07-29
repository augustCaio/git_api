"""
Modelos Pydantic para dados do GitHub
"""

from .github_models import (
    GitHubUser,
    GitHubRepository,
    GitHubLanguage,
    GitHubEvent,
    GitHubCommit,
    GitHubIssue,
    GitHubPullRequest,
)

from .response_models import (
    APIResponse,
    ErrorResponse,
    PaginatedResponse,
    UserStatsResponse,
    UserLanguagesResponse,
    HealthResponse,
)

__all__ = [
    "GitHubUser",
    "GitHubRepository", 
    "GitHubLanguage",
    "GitHubEvent",
    "GitHubCommit",
    "GitHubIssue",
    "GitHubPullRequest",
    "APIResponse",
    "ErrorResponse",
    "PaginatedResponse",
    "UserStatsResponse",
    "UserLanguagesResponse",
    "HealthResponse",
] 