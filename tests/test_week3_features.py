"""
Testes para as funcionalidades da Semana 3 - Performance e Deploy
"""

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.services.cache_service import CacheService, cache_service
from app.utils.logger import logger

client = TestClient(app)


class TestCacheService:
    """Testes para o serviço de cache"""
    
    def test_cache_service_initialization(self):
        """Testa inicialização do serviço de cache"""
        cache = CacheService()
        assert cache.memory_cache is not None
        assert cache.use_redis is False  # Redis desabilitado por padrão
    
    def test_cache_set_and_get(self):
        """Testa operações básicas de cache"""
        cache = CacheService()
        
        # Testa set e get
        cache.set("test_key", "test_value", ttl=60)
        value = cache.get("test_key")
        assert value == "test_value"
    
    def test_cache_delete(self):
        """Testa remoção de cache"""
        cache = CacheService()
        
        # Adiciona valor
        cache.set("test_key", "test_value")
        assert cache.get("test_key") == "test_value"
        
        # Remove valor
        success = cache.delete("test_key")
        assert success is True
        assert cache.get("test_key") is None
    
    def test_cache_clear(self):
        """Testa limpeza do cache"""
        cache = CacheService()
        
        # Adiciona valores
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        
        # Limpa cache
        success = cache.clear()
        assert success is True
        assert cache.get("key1") is None
        assert cache.get("key2") is None
    
    def test_cache_get_or_set(self):
        """Testa get_or_set"""
        cache = CacheService()
        
        # Primeira chamada - executa função
        def get_value():
            return "computed_value"
        
        value = cache.get_or_set("test_key", get_value, ttl=60)
        assert value == "computed_value"
        
        # Segunda chamada - retorna do cache
        value = cache.get_or_set("test_key", get_value, ttl=60)
        assert value == "computed_value"
    
    def test_cache_stats(self):
        """Testa estatísticas do cache"""
        cache = CacheService()
        
        # Adiciona alguns valores
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        
        stats = cache.get_stats()
        assert "memory_cache_size" in stats
        assert "memory_cache_maxsize" in stats
        assert "use_redis" in stats
        assert "redis_connected" in stats


class TestCacheEndpoints:
    """Testes para endpoints de cache"""
    
    def test_cache_stats_endpoint(self):
        """Testa endpoint de estatísticas do cache"""
        response = client.get("/api/v1/cache/stats")
        assert response.status_code == 200
        
        data = response.json()
        assert "memory_cache_size" in data
        assert "memory_cache_maxsize" in data
        assert "use_redis" in data
        assert "redis_connected" in data
    
    def test_cache_clear_endpoint(self):
        """Testa endpoint de limpeza do cache"""
        response = client.delete("/api/v1/cache/clear")
        assert response.status_code == 200
        
        data = response.json()
        assert "success" in data
        assert "message" in data


class TestEnhancedHealthCheck:
    """Testes para health check melhorado"""
    
    def test_health_check_with_cache_info(self):
        """Testa health check com informações de cache"""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert "message" in data
        assert "version" in data
        assert "timestamp" in data
        assert "cache" in data
        assert "environment" in data
    
    def test_health_check_headers(self):
        """Testa headers de performance no health check"""
        response = client.get("/api/v1/health")
        
        # Verifica headers de performance
        assert "X-Request-ID" in response.headers
        assert "X-Response-Time" in response.headers
        
        # Verifica que o tempo de resposta é um número
        response_time = float(response.headers["X-Response-Time"])
        assert response_time >= 0


class TestLoggingMiddleware:
    """Testes para middleware de logging"""
    
    def test_request_logging_headers(self):
        """Testa se headers de logging são adicionados"""
        response = client.get("/api/v1/health")
        
        # Verifica headers de logging
        assert "X-Request-ID" in response.headers
        assert "X-Response-Time" in response.headers
        
        # Verifica formato do Request ID (UUID)
        request_id = response.headers["X-Request-ID"]
        assert len(request_id) == 36  # UUID v4 tem 36 caracteres
    
    def test_multiple_requests_have_different_ids(self):
        """Testa se requisições diferentes têm IDs únicos"""
        response1 = client.get("/api/v1/health")
        response2 = client.get("/api/v1/health")
        
        request_id1 = response1.headers["X-Request-ID"]
        request_id2 = response2.headers["X-Request-ID"]
        
        assert request_id1 != request_id2


class TestCacheIntegration:
    """Testes de integração com cache"""
    
    @patch('app.services.github_client.GitHubClient._make_request')
    def test_user_endpoint_with_cache(self, mock_make_request):
        """Testa endpoint de usuário com cache"""
        # Mock da resposta da API
        mock_response = {
            "id": 1,
            "login": "testuser",
            "name": "Test User",
            "public_repos": 5,
            "followers": 10,
            "following": 5,
            "type": "User",
            "site_admin": False
        }
        mock_make_request.return_value = mock_response
        
        # Primeira requisição - deve buscar da API
        response1 = client.get("/api/v1/users/testuser")
        assert response1.status_code == 200
        
        # Segunda requisição - deve vir do cache (mais rápida)
        response2 = client.get("/api/v1/users/testuser")
        assert response2.status_code == 200
        
        # Verifica que a API foi chamada apenas uma vez
        mock_make_request.assert_called_once()
        
        # Verifica que o tempo da segunda requisição é menor
        time1 = float(response1.headers["X-Response-Time"])
        time2 = float(response2.headers["X-Response-Time"])
        assert time2 < time1


class TestErrorHandling:
    """Testes para tratamento de erros"""
    
    def test_invalid_cache_key(self):
        """Testa comportamento com chave de cache inválida"""
        cache = CacheService()
        
        # Testa com chave None
        assert cache.get(None) is None
        # O cache aceita chaves None, então o teste deve verificar isso
        assert cache.set(None, "value") is True
    
    def test_cache_with_complex_objects(self):
        """Testa cache com objetos complexos"""
        cache = CacheService()
        
        complex_obj = {
            "user": {"id": 1, "name": "Test"},
            "repos": [{"id": 1, "name": "repo1"}],
            "metadata": {"timestamp": "2023-01-01"}
        }
        
        # Testa serialização/deserialização
        cache.set("complex_key", complex_obj)
        retrieved = cache.get("complex_key")
        
        assert retrieved == complex_obj


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 