"""Conexão e verificação básica do Redis."""

from functools import lru_cache

from redis import Redis

from config import REDIS_DATABASE, REDIS_HOST, REDIS_PASSWORD, REDIS_PORT


@lru_cache(maxsize=1)
def get_client() -> Redis:
    """Retorna um cliente Redis reutilizável."""
    return Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DATABASE,
        password=REDIS_PASSWORD,
        decode_responses=True,
        socket_connect_timeout=5,
        socket_timeout=5,
    )


def check_connection() -> None:
    """Falha se o Redis não responder ao comando ping."""
    if not get_client().ping():
        raise ConnectionError("O Redis não confirmou o ping.")


def close_connection() -> None:
    """Fecha o cliente e permite criá-lo novamente depois."""
    if get_client.cache_info().currsize:
        get_client().close()
        get_client.cache_clear()
