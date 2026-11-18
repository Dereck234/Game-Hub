"""Conexão e verificação básica do MongoDB."""

from functools import lru_cache

from pymongo import MongoClient

from config import MONGODB_URI


@lru_cache(maxsize=1)
def get_client() -> MongoClient:
    """Retorna um cliente MongoDB reutilizável."""
    return MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)


def check_connection() -> None:
    """Falha se o MongoDB não responder ao comando ping."""
    get_client().admin.command("ping")


def close_connection() -> None:
    """Fecha o cliente e permite criá-lo novamente depois."""
    if get_client.cache_info().currsize:
        get_client().close()
        get_client.cache_clear()
