"""Consultas do catálogo e cache individual de jogos."""

import json
import re

from bson import json_util

from config import MONGODB_DATABASE
from database.mongodb import get_client
from database.redis_db import get_client as get_redis

CACHE_TTL_SECONDS = 60


def listar_jogos(busca: str = "", categoria: str = "Todas") -> list[dict]:
    query: dict = {}
    if busca.strip():
        query["nome"] = {"$regex": re.escape(busca.strip()), "$options": "i"}
    if categoria and categoria != "Todas":
        query["categorias"] = categoria
    return list(get_client()[MONGODB_DATABASE].jogos.find(query).sort("nome", 1))


def listar_categorias() -> list[str]:
    return sorted(get_client()[MONGODB_DATABASE].jogos.distinct("categorias"))


def obter_jogo(jogo_id: str) -> dict | None:
    cache = get_redis()
    key = f"gamehub:produto:{jogo_id}"
    cached = cache.get(key)
    if cached:
        return json_util.loads(cached)
    game = get_client()[MONGODB_DATABASE].jogos.find_one({"_id": jogo_id})
    if game:
        cache.set(key, json_util.dumps(game), ex=CACHE_TTL_SECONDS)
    return game


def listar_clientes() -> list[dict]:
    return list(get_client()[MONGODB_DATABASE].clientes.find({}, {"nome": 1}).sort("nome", 1))
