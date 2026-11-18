"""Operações do carrinho armazenado no Redis."""

from config import MONGODB_DATABASE
from database.mongodb import get_client as get_mongo
from database.redis_db import get_client


def _key(cliente_id: str) -> str:
    return f"gamehub:carrinho:{cliente_id}"


def _assert_editable(cliente_id: str) -> None:
    pending = get_mongo()[MONGODB_DATABASE].pedidos.find_one(
        {"cliente_id": cliente_id, "status": "PENDENTE"}, {"_id": 1}
    )
    if pending:
        raise RuntimeError("Retome o pedido pendente antes de alterar o carrinho.")


def obter_itens(cliente_id: str) -> dict[str, int]:
    return {jogo_id: int(quantidade) for jogo_id, quantidade in get_client().hgetall(_key(cliente_id)).items()}


def adicionar(cliente_id: str, jogo_id: str, quantidade: int = 1) -> None:
    _assert_editable(cliente_id)
    if quantidade < 1:
        raise ValueError("A quantidade deve ser maior que zero.")
    get_client().hincrby(_key(cliente_id), jogo_id, quantidade)


def definir_quantidade(cliente_id: str, jogo_id: str, quantidade: int) -> None:
    _assert_editable(cliente_id)
    if quantidade < 1:
        raise ValueError("A quantidade deve ser maior que zero.")
    get_client().hset(_key(cliente_id), jogo_id, quantidade)


def remover(cliente_id: str, jogo_id: str) -> None:
    _assert_editable(cliente_id)
    get_client().hdel(_key(cliente_id), jogo_id)


def limpar(cliente_id: str) -> None:
    get_client().delete(_key(cliente_id))
