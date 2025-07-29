"""
Serviço de cache para a API
"""

import json
import hashlib
from typing import Any, Optional, Union
from datetime import datetime, timedelta
from cachetools import TTLCache
import redis
from app.config import settings


class CacheService:
    """Serviço de cache com suporte a cache em memória e Redis"""
    
    def __init__(self):
        self.memory_cache = TTLCache(maxsize=1000, ttl=300)  # 5 minutos por padrão
        self.redis_client = None
        self.use_redis = settings.use_redis_cache
        
        if self.use_redis:
            self._init_redis()
    
    def _init_redis(self):
        """Inicializa conexão com Redis"""
        try:
            self.redis_client = redis.Redis(
                host=settings.redis_host,
                port=settings.redis_port,
                password=settings.redis_password,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5
            )
            # Testa conexão
            self.redis_client.ping()
            print("✅ Redis conectado com sucesso")
        except Exception as e:
            print(f"⚠️  Redis não disponível, usando cache em memória: {e}")
            self.use_redis = False
            self.redis_client = None
    
    def _generate_key(self, prefix: str, *args, **kwargs) -> str:
        """Gera chave única para cache"""
        # Combina prefixo com argumentos
        key_parts = [prefix]
        
        # Adiciona argumentos posicionais
        for arg in args:
            key_parts.append(str(arg))
        
        # Adiciona argumentos nomeados ordenados
        for key, value in sorted(kwargs.items()):
            key_parts.append(f"{key}:{value}")
        
        # Cria hash da chave
        key_string = "|".join(key_parts)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """Obtém valor do cache"""
        try:
            if self.use_redis and self.redis_client:
                # Tenta Redis primeiro
                value = self.redis_client.get(key)
                if value:
                    return json.loads(value)
            
            # Fallback para cache em memória
            return self.memory_cache.get(key)
            
        except Exception as e:
            print(f"⚠️  Erro ao obter cache: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: int = 300) -> bool:
        """Define valor no cache"""
        try:
            if self.use_redis and self.redis_client:
                # Tenta Redis primeiro
                serialized_value = json.dumps(value, default=str)
                return self.redis_client.setex(key, ttl, serialized_value)
            
            # Fallback para cache em memória
            self.memory_cache[key] = value
            return True
            
        except Exception as e:
            print(f"⚠️  Erro ao definir cache: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Remove valor do cache"""
        try:
            if self.use_redis and self.redis_client:
                return bool(self.redis_client.delete(key))
            
            # Fallback para cache em memória
            return self.memory_cache.pop(key, None) is not None
            
        except Exception as e:
            print(f"⚠️  Erro ao deletar cache: {e}")
            return False
    
    def clear(self) -> bool:
        """Limpa todo o cache"""
        try:
            if self.use_redis and self.redis_client:
                self.redis_client.flushdb()
            
            # Limpa cache em memória
            self.memory_cache.clear()
            return True
            
        except Exception as e:
            print(f"⚠️  Erro ao limpar cache: {e}")
            return False
    
    def get_or_set(self, key: str, default_func, ttl: int = 300) -> Any:
        """Obtém valor do cache ou executa função padrão"""
        value = self.get(key)
        if value is not None:
            return value
        
        # Executa função padrão
        value = default_func()
        self.set(key, value, ttl)
        return value
    
    def cache_decorator(self, prefix: str, ttl: int = 300):
        """Decorator para cache automático"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                # Gera chave única
                cache_key = self._generate_key(prefix, *args, **kwargs)
                
                # Tenta obter do cache
                cached_value = self.get(cache_key)
                if cached_value is not None:
                    return cached_value
                
                # Executa função e armazena no cache
                result = func(*args, **kwargs)
                self.set(cache_key, result, ttl)
                return result
            
            return wrapper
        return decorator
    
    def get_stats(self) -> dict:
        """Retorna estatísticas do cache"""
        stats = {
            "memory_cache_size": len(self.memory_cache),
            "memory_cache_maxsize": self.memory_cache.maxsize,
            "use_redis": self.use_redis,
            "redis_connected": False
        }
        
        if self.use_redis and self.redis_client:
            try:
                info = self.redis_client.info()
                stats["redis_connected"] = True
                stats["redis_used_memory"] = info.get("used_memory_human", "N/A")
                stats["redis_keyspace_hits"] = info.get("keyspace_hits", 0)
                stats["redis_keyspace_misses"] = info.get("keyspace_misses", 0)
            except Exception:
                stats["redis_connected"] = False
        
        return stats


# Instância global do serviço de cache
cache_service = CacheService() 