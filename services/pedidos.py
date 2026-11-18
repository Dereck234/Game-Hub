"""Checkout simples com retomada idempotente entre MongoDB e Neo4j."""

from datetime import datetime, timezone
from uuid import uuid4

from pymongo.errors import DuplicateKeyError

from config import MONGODB_DATABASE, NEO4J_DATABASE
from database.mongodb import get_client as get_mongo
from database.neo4j_db import get_driver
from services.carrinho import limpar, obter_itens


class CheckoutError(Exception):
    """Erro de validação do checkout."""


def obter_pedido_pendente(cliente_id: str) -> dict | None:
    return get_mongo()[MONGODB_DATABASE].pedidos.find_one(
        {"cliente_id": cliente_id, "status": "PENDENTE"}
    )


def _registrar_compras(pedido: dict) -> None:
    query = """
    MATCH (cliente:Cliente {id: $cliente_id})
    UNWIND $itens AS item
    MATCH (produto:Produto {id: item.jogo_id})
    MERGE (cliente)-[compra:COMPROU {checkout_id: $checkout_id}]->(produto)
    SET compra.data = $data
    RETURN count(compra) AS processadas
    """
    with get_driver().session(database=NEO4J_DATABASE) as session:
        result = session.run(
            query,
            cliente_id=pedido["cliente_id"],
            checkout_id=pedido["checkout_id"],
            data=pedido["data_criacao"].isoformat(),
            itens=pedido["itens"],
        ).single()
    if not result or result["processadas"] != len(pedido["itens"]):
        raise RuntimeError("O Neo4j não confirmou todas as relações de compra.")


def finalizar(cliente_id: str, checkout_id: str | None = None) -> dict:
    database = get_mongo()[MONGODB_DATABASE]
    checkout_id = checkout_id or str(uuid4())
    pedido = database.pedidos.find_one({"checkout_id": checkout_id})
    if pedido and pedido["cliente_id"] != cliente_id:
        raise CheckoutError("Este identificador pertence a outro cliente.")

    if pedido is None:
        if obter_pedido_pendente(cliente_id):
            raise CheckoutError("Retome o pedido pendente antes de iniciar outro checkout.")
        cart = obter_itens(cliente_id)
        if not cart:
            raise CheckoutError("O carrinho está vazio.")
        jogos = database.jogos
        itens = []
        total = 0.0
        for jogo_id, quantidade in cart.items():
            jogo = jogos.find_one({"_id": jogo_id})
            if not jogo:
                raise CheckoutError(f"O jogo {jogo_id} não existe mais no catálogo.")
            preco = float(jogo["preco"])
            itens.append({
                "jogo_id": jogo_id,
                "nome": jogo["nome"],
                "quantidade": quantidade,
                "preco_unitario": preco,
            })
            total += preco * quantidade
        pedido = {
            "checkout_id": checkout_id,
            "cliente_id": cliente_id,
            "itens": itens,
            "total": round(total, 2),
            "status": "PENDENTE",
            "data_criacao": datetime.now(timezone.utc),
        }
        try:
            database.pedidos.insert_one(pedido)
        except DuplicateKeyError:
            pedido = database.pedidos.find_one({"checkout_id": checkout_id})
            if not pedido or pedido["cliente_id"] != cliente_id:
                raise CheckoutError("Não foi possível confirmar a tentativa de checkout.")

    if pedido["status"] == "PENDENTE":
        _registrar_compras(pedido)
        database.pedidos.update_one(
            {"checkout_id": checkout_id, "status": "PENDENTE"},
            {"$set": {"status": "CONCLUIDO"}},
        )
        pedido["status"] = "CONCLUIDO"

    if pedido["status"] == "CONCLUIDO":
        limpar(cliente_id)
    return pedido
