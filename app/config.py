"""
Configurações da aplicação usando Pydantic Settings
"""

from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict


class Settings(BaseSettings):
    """Configurações da aplicação"""
    
    # Configurações da API
    api_title: str = Field(default="GitHub Data API", alias="API_TITLE")
    api_version: str = Field(default="0.1.0", alias="API_VERSION")
    api_description: str = Field(default="API para captura de dados do GitHub", alias="API_DESCRIPTION")
    
    # Configurações do servidor
    host: str = Field(default="127.0.0.1", alias="HOST")
    port: int = Field(default=8000, alias="PORT")
    debug: bool = Field(default=True, alias="DEBUG")
    
    # GitHub API
    github_token: Optional[str] = Field(default=None, alias="GITHUB_TOKEN")
    github_api_base_url: str = Field(default="https://api.github.com", alias="GITHUB_API_BASE_URL")
    
    # Configurações de segurança
    secret_key: str = Field(default="sua-chave-secreta-aqui-mude-em-producao", alias="SECRET_KEY")
    algorithm: str = Field(default="HS256", alias="ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # Configurações de API Key (opcional)
    enable_api_key_auth: bool = Field(default=False, alias="ENABLE_API_KEY_AUTH")
    api_key_header: str = Field(default="X-API-Key", alias="API_KEY_HEADER")
    valid_api_keys: list = Field(default=[], alias="VALID_API_KEYS")
    
    # Configurações de rate limiting
    rate_limit_per_minute: int = Field(default=60, alias="RATE_LIMIT_PER_MINUTE")
    
    # Configurações de Cache
    use_redis_cache: bool = Field(default=False, alias="USE_REDIS_CACHE")
    redis_host: str = Field(default="localhost", alias="REDIS_HOST")
    redis_port: int = Field(default=6379, alias="REDIS_PORT")
    redis_password: Optional[str] = Field(default=None, alias="REDIS_PASSWORD")
    cache_ttl: int = Field(default=300, alias="CACHE_TTL")  # 5 minutos por padrão
    
    model_config = ConfigDict(
        env_file="config.env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        populate_by_name=True
    )


# Instância global das configurações
settings = Settings() 