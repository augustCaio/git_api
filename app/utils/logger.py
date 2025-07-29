"""
Sistema de logging estruturado com loguru
"""

import sys
import json
from datetime import datetime
from pathlib import Path
from loguru import logger
from app.config import settings


def setup_logging():
    """Configura o sistema de logging"""

    # Remove logger padrão
    logger.remove()

    # Configuração para console (desenvolvimento)
    if settings.debug:
        logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level="DEBUG",
            colorize=True
        )
    else:
        # Configuração para produção (JSON estruturado)
        logger.add(
            sys.stdout,
            format=lambda record: json.dumps({
                "timestamp": record["time"].isoformat(),
                "level": record["level"].name,
                "logger": record["name"],
                "function": record["function"],
                "line": record["line"],
                "message": record["message"],
                "extra": record["extra"],
                "service": "github-data-api",
                "version": settings.api_version,
                "environment": "production"
            }),
            level="INFO",
            serialize=True
        )

    # Configuração para arquivo de logs (produção)
    if not settings.debug:
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        # Log de aplicação (produção)
        logger.add(
            log_dir / "app.log",
            format=lambda record: json.dumps({
                "timestamp": record["time"].isoformat(),
                "level": record["level"].name,
                "logger": record["name"],
                "function": record["function"],
                "line": record["line"],
                "message": record["message"],
                "extra": record["extra"],
                "service": "github-data-api",
                "version": settings.api_version,
                "environment": "production"
            }),
            level="INFO",
            rotation="10 MB",
            retention="30 days",
            compression="zip",
            serialize=True
        )

        # Log de erros (produção)
        logger.add(
            log_dir / "error.log",
            format=lambda record: json.dumps({
                "timestamp": record["time"].isoformat(),
                "level": record["level"].name,
                "logger": record["name"],
                "function": record["function"],
                "line": record["line"],
                "message": record["message"],
                "extra": record["extra"],
                "service": "github-data-api",
                "version": settings.api_version,
                "environment": "production"
            }),
            level="ERROR",
            rotation="10 MB",
            retention="90 days",
            compression="zip",
            serialize=True
        )

        # Log de performance (produção)
        logger.add(
            log_dir / "performance.log",
            format=lambda record: json.dumps({
                "timestamp": record["time"].isoformat(),
                "level": record["level"].name,
                "logger": record["name"],
                "function": record["function"],
                "line": record["line"],
                "message": record["message"],
                "extra": record["extra"],
                "service": "github-data-api",
                "version": settings.api_version,
                "environment": "production"
            }),
            level="INFO",
            filter=lambda record: "performance" in record["extra"],
            rotation="10 MB",
            retention="30 days",
            compression="zip",
            serialize=True
        )
    
    # Configuração para arquivo de logs
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Log de aplicação
    logger.add(
        log_dir / "app.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="INFO",
        rotation="10 MB",
        retention="30 days",
        compression="zip"
    )
    
    # Log de erros
    logger.add(
        log_dir / "error.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="ERROR",
        rotation="10 MB",
        retention="90 days",
        compression="zip"
    )
    
    # Log de performance
    logger.add(
        log_dir / "performance.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="INFO",
        filter=lambda record: "performance" in record["extra"],
        rotation="10 MB",
        retention="30 days",
        compression="zip"
    )


def log_request(request_id: str, method: str, url: str, status_code: int, duration: float):
    """Log de requisições HTTP"""
    logger.info(
        f"Request {request_id}: {method} {url} - {status_code} ({duration:.3f}s)",
        extra={
            "request_id": request_id,
            "method": method,
            "url": url,
            "status_code": status_code,
            "duration": duration,
            "type": "http_request"
        }
    )


def log_cache_hit(key: str, ttl: int):
    """Log de cache hit"""
    logger.info(
        f"Cache HIT: {key} (TTL: {ttl}s)",
        extra={
            "cache_key": key,
            "cache_ttl": ttl,
            "type": "cache_hit"
        }
    )


def log_cache_miss(key: str):
    """Log de cache miss"""
    logger.info(
        f"Cache MISS: {key}",
        extra={
            "cache_key": key,
            "type": "cache_miss"
        }
    )


def log_github_api_call(endpoint: str, duration: float, status_code: int = None):
    """Log de chamadas para API do GitHub"""
    logger.info(
        f"GitHub API: {endpoint} ({duration:.3f}s)",
        extra={
            "github_endpoint": endpoint,
            "duration": duration,
            "status_code": status_code,
            "type": "github_api"
        }
    )


def log_error(error: Exception, context: dict = None):
    """Log de erros"""
    logger.error(
        f"Error: {str(error)}",
        extra={
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context or {},
            "type": "error"
        }
    )


def log_performance(operation: str, duration: float, details: dict = None):
    """Log de performance"""
    logger.info(
        f"Performance: {operation} ({duration:.3f}s)",
        extra={
            "operation": operation,
            "duration": duration,
            "details": details or {},
            "type": "performance"
        }
    )


# Configura logging na inicialização
setup_logging() 