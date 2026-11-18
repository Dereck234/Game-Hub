"""Conexão e verificação básica do Neo4j."""

from functools import lru_cache

from neo4j import Driver, GraphDatabase

from config import NEO4J_DATABASE, NEO4J_PASSWORD, NEO4J_URI, NEO4J_USER


@lru_cache(maxsize=1)
def get_driver() -> Driver:
    """Retorna um driver Neo4j reutilizável."""
    return GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


def check_connection() -> None:
    """Verifica a conexão e executa uma consulta sem alterar dados."""
    driver = get_driver()
    driver.verify_connectivity()
    with driver.session(database=NEO4J_DATABASE) as session:
        session.run("RETURN 1 AS ok").consume()


def close_connection() -> None:
    """Fecha o driver e permite criá-lo novamente depois."""
    if get_driver.cache_info().currsize:
        get_driver().close()
        get_driver.cache_clear()
