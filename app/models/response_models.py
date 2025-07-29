"""
Modelos de resposta padronizados para a API
"""

from typing import Generic, TypeVar, Optional, Any, Dict, List
from pydantic import BaseModel, Field
from datetime import datetime

T = TypeVar('T')


class APIResponse(BaseModel, Generic[T]):
    """Modelo base para respostas da API"""
    success: bool = Field(description="Indica se a operação foi bem-sucedida")
    message: str = Field(description="Mensagem descritiva da resposta")
    data: Optional[T] = Field(default=None, description="Dados da resposta")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp da resposta")
    path: Optional[str] = Field(default=None, description="Caminho da requisição")


class ErrorResponse(BaseModel):
    """Modelo para respostas de erro"""
    success: bool = Field(default=False, description="Sempre false para erros")
    error: str = Field(description="Tipo do erro")
    message: str = Field(description="Mensagem de erro detalhada")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp do erro")
    path: Optional[str] = Field(default=None, description="Caminho da requisição")


class PaginatedResponse(BaseModel, Generic[T]):
    """Modelo para respostas paginadas"""
    success: bool = Field(default=True, description="Indica se a operação foi bem-sucedida")
    message: str = Field(description="Mensagem descritiva da resposta")
    data: List[T] = Field(description="Lista de dados")
    pagination: Dict[str, Any] = Field(description="Informações de paginação")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp da resposta")
    path: Optional[str] = Field(default=None, description="Caminho da requisição")


class UserStatsResponse(BaseModel):
    """Modelo para resposta de estatísticas do usuário"""
    username: str = Field(description="Nome do usuário")
    user: Dict[str, Any] = Field(description="Dados do usuário")
    repositories: Dict[str, int] = Field(description="Estatísticas de repositórios")
    activity: Dict[str, Any] = Field(description="Estatísticas de atividade")
    languages: Dict[str, Any] = Field(description="Estatísticas de linguagens")
    top_repositories: List[Dict[str, Any]] = Field(description="Top repositórios")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp da resposta")


class UserLanguagesResponse(BaseModel):
    """Modelo para resposta de linguagens do usuário"""
    username: str = Field(description="Nome do usuário")
    languages: Dict[str, Any] = Field(description="Linguagens e estatísticas")
    total_languages: int = Field(description="Total de linguagens")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp da resposta")


class HealthResponse(BaseModel):
    """Modelo para resposta de health check"""
    status: str = Field(description="Status da API")
    message: str = Field(description="Mensagem de status")
    version: str = Field(description="Versão da API")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp da resposta")
    uptime: Optional[float] = Field(default=None, description="Tempo de atividade em segundos") 