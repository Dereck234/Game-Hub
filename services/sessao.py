"""Token temporário para a sessão demonstrativa."""

from uuid import uuid4

from database.redis_db import get_client

SESSION_TTL_SECONDS = 30 * 60


def criar_sessao(cliente_id: str) -> str:
    token = str(uuid4())
    get_client().set(f"gamehub:token_demo:{token}", cliente_id, ex=SESSION_TTL_SECONDS)
    return token


def obter_cliente(token: str) -> str | None:
    return get_client().get(f"gamehub:token_demo:{token}") if token else None
