"""
Utilitários de autenticação para a API
"""

from typing import Optional
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import settings
from app.utils.logger import logger
import time


class OptionalAPIKeyAuth:
    """Autenticação opcional por API Key"""
    
    def __init__(self):
        self.enable_auth = settings.enable_api_key_auth
        self.api_key_header = settings.api_key_header
        self.valid_keys = settings.valid_api_keys
    
    async def __call__(self, request: Request) -> Optional[str]:
        """
        Verifica se a API Key é válida (se a autenticação estiver habilitada)
        
        Args:
            request: Requisição FastAPI
            
        Returns:
            API Key se válida, None se autenticação desabilitada
            
        Raises:
            HTTPException: Se API Key inválida
        """
        if not self.enable_auth:
            return None
        
        # Obtém a API Key do header
        api_key = request.headers.get(self.api_key_header)
        
        if not api_key:
            logger.warning(f"API Key não fornecida no header {self.api_key_header}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"API Key obrigatória no header {self.api_key_header}",
                headers={"WWW-Authenticate": f"{self.api_key_header} realm=\"API\""}
            )
        
        # Verifica se a API Key é válida
        if api_key not in self.valid_keys:
            logger.warning(f"API Key inválida fornecida: {api_key[:8]}...")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="API Key inválida",
                headers={"WWW-Authenticate": f"{self.api_key_header} realm=\"API\""}
            )
        
        logger.info(f"API Key válida fornecida: {api_key[:8]}...")
        return api_key


class RateLimitMiddleware:
    """Middleware para rate limiting básico"""
    
    def __init__(self):
        self.requests_per_minute = settings.rate_limit_per_minute
        self.request_counts = {}  # Em produção, use Redis
    
    async def check_rate_limit(self, request: Request) -> bool:
        """
        Verifica se a requisição está dentro do rate limit
        
        Args:
            request: Requisição FastAPI
            
        Returns:
            True se permitido, False se excedeu o limite
        """
        # Identifica o cliente (IP ou API Key)
        client_id = self._get_client_id(request)
        
        # Implementação básica - em produção use Redis
        current_time = int(time.time() / 60)  # Minuto atual
        
        if client_id not in self.request_counts:
            self.request_counts[client_id] = {}
        
        if current_time not in self.request_counts[client_id]:
            self.request_counts[client_id][current_time] = 0
        
        self.request_counts[client_id][current_time] += 1
        
        # Verifica se excedeu o limite
        if self.request_counts[client_id][current_time] > self.requests_per_minute:
            logger.warning(f"Rate limit excedido para cliente: {client_id}")
            return False
        
        return True
    
    def _get_client_id(self, request: Request) -> str:
        """Obtém identificador único do cliente"""
        # Prioriza API Key, depois IP
        api_key = request.headers.get(settings.api_key_header)
        if api_key:
            return f"api_key:{api_key[:8]}"
        
        # IP do cliente
        client_ip = request.client.host if request.client else "unknown"
        return f"ip:{client_ip}"


# Instâncias globais
api_key_auth = OptionalAPIKeyAuth()
rate_limit = RateLimitMiddleware() 