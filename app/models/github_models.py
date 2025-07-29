"""
Modelos Pydantic para dados do GitHub
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, HttpUrl


class GitHubUser(BaseModel):
    """Modelo para dados de usuário do GitHub"""
    id: int
    login: str
    name: Optional[str] = None
    email: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    company: Optional[str] = None
    blog: Optional[str] = None
    twitter_username: Optional[str] = None
    public_repos: int = 0
    public_gists: int = 0
    followers: int = 0
    following: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    hireable: Optional[bool] = None
    type: str = "User"
    site_admin: bool = False


class GitHubRepository(BaseModel):
    """Modelo para dados de repositório do GitHub"""
    id: int
    name: str
    full_name: str
    description: Optional[str] = None
    private: bool = False
    fork: bool = False
    language: Optional[str] = None
    size: int = 0
    stargazers_count: int = 0
    watchers_count: int = 0
    forks_count: int = 0
    open_issues_count: int = 0
    default_branch: str = "main"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    pushed_at: Optional[datetime] = None
    homepage: Optional[str] = None
    topics: List[str] = Field(default_factory=list)
    archived: bool = False
    disabled: bool = False
    license: Optional[Dict[str, Any]] = None
    owner: Optional[GitHubUser] = None


class GitHubLanguage(BaseModel):
    """Modelo para dados de linguagem de programação"""
    name: str
    bytes: int
    percentage: float = 0.0


class GitHubEvent(BaseModel):
    """Modelo para eventos do GitHub"""
    id: str
    type: str
    actor: Optional[GitHubUser] = None
    repo: Optional[Dict[str, Any]] = None
    payload: Optional[Dict[str, Any]] = None
    public: bool = True
    created_at: Optional[datetime] = None


class GitHubCommit(BaseModel):
    """Modelo para commits do GitHub"""
    sha: str
    node_id: str
    commit: Dict[str, Any]
    url: HttpUrl
    html_url: HttpUrl
    comments_url: HttpUrl
    author: Optional[GitHubUser] = None
    committer: Optional[GitHubUser] = None
    parents: List[Dict[str, Any]] = Field(default_factory=list)


class GitHubIssue(BaseModel):
    """Modelo para issues do GitHub"""
    id: int
    number: int
    title: str
    body: Optional[str] = None
    state: str
    locked: bool = False
    assignee: Optional[GitHubUser] = None
    assignees: List[GitHubUser] = Field(default_factory=list)
    milestone: Optional[Dict[str, Any]] = None
    comments: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    author_association: str = "NONE"
    user: Optional[GitHubUser] = None
    labels: List[Dict[str, Any]] = Field(default_factory=list)


class GitHubPullRequest(BaseModel):
    """Modelo para Pull Requests do GitHub"""
    id: int
    number: int
    title: str
    body: Optional[str] = None
    state: str
    locked: bool = False
    assignee: Optional[GitHubUser] = None
    assignees: List[GitHubUser] = Field(default_factory=list)
    requested_reviewers: List[GitHubUser] = Field(default_factory=list)
    milestone: Optional[Dict[str, Any]] = None
    comments: int = 0
    review_comments: int = 0
    commits: int = 0
    additions: int = 0
    deletions: int = 0
    changed_files: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    merged_at: Optional[datetime] = None
    merge_commit_sha: Optional[str] = None
    author_association: str = "NONE"
    user: Optional[GitHubUser] = None
    labels: List[Dict[str, Any]] = Field(default_factory=list)
    head: Dict[str, Any]
    base: Dict[str, Any]
    draft: bool = False
    merged: bool = False
    mergeable: Optional[bool] = None
    mergeable_state: str = "unknown"
    merged_by: Optional[GitHubUser] = None
    comments_url: HttpUrl
    review_comments_url: HttpUrl
    commits_url: HttpUrl
    statuses_url: HttpUrl 