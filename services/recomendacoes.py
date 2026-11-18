"""Recomendações calculadas por consulta Cypher no Neo4j."""

from config import NEO4J_DATABASE
from database.neo4j_db import get_driver


def recomendar(cliente_id: str, limite: int = 5) -> list[dict]:
    query = """
    MATCH (cliente:Cliente {id: $cliente_id})
    MATCH (cliente)-[:COMPROU]->(compartilhado:Produto)<-[:COMPROU]-(similar:Cliente)
    WHERE similar <> cliente
    MATCH (similar)-[:COMPROU]->(candidato:Produto)
    MATCH (similar)-[avaliacao:AVALIOU]->(candidato)
    WHERE avaliacao.nota >= 4
      AND NOT (cliente)-[:COMPROU]->(candidato)
    WITH candidato, count(DISTINCT similar) AS relevancia
    RETURN candidato.id AS id, candidato.nome AS nome, candidato.preco AS preco,
           relevancia
    ORDER BY relevancia DESC, nome ASC
    LIMIT $limite
    """
    with get_driver().session(database=NEO4J_DATABASE) as session:
        return [record.data() for record in session.run(query, cliente_id=cliente_id, limite=limite)]
