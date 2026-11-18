"""Carrega configurações dos bancos a partir do ambiente ou de .env."""

import os
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()


def _required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"A variável de ambiente {name} é obrigatória.")
    return value


def _integer(name: str, default: int) -> int:
    value = os.getenv(name, str(default))
    try:
        return int(value)
    except ValueError as error:
        raise RuntimeError(f"A variável {name} deve conter um número inteiro.") from error


MONGODB_HOST = os.getenv("MONGODB_HOST", "localhost")
MONGODB_PORT = _integer("MONGODB_PORT", 27017)
MONGODB_ROOT_USERNAME = _required("MONGODB_ROOT_USERNAME")
MONGODB_ROOT_PASSWORD = _required("MONGODB_ROOT_PASSWORD")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "gamehub")
MONGODB_AUTH_SOURCE = os.getenv("MONGODB_AUTH_SOURCE", "admin")

MONGODB_URI = (
    f"mongodb://{quote_plus(MONGODB_ROOT_USERNAME)}:"
    f"{quote_plus(MONGODB_ROOT_PASSWORD)}@{MONGODB_HOST}:{MONGODB_PORT}/"
    f"{MONGODB_DATABASE}?authSource={quote_plus(MONGODB_AUTH_SOURCE)}"
)

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = _integer("REDIS_PORT", 6379)
REDIS_PASSWORD = _required("REDIS_PASSWORD")
REDIS_DATABASE = _integer("REDIS_DATABASE", 0)

NEO4J_HOST = os.getenv("NEO4J_HOST", "localhost")
NEO4J_BOLT_PORT = _integer("NEO4J_BOLT_PORT", 7687)
NEO4J_URI = f"bolt://{NEO4J_HOST}:{NEO4J_BOLT_PORT}"
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
if NEO4J_USER != "neo4j":
    raise RuntimeError("A imagem do Neo4j utilizada exige o usuário inicial 'neo4j'.")
NEO4J_PASSWORD = _required("NEO4J_PASSWORD")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")
