"""Carrega dados demonstrativos de forma repetível no MongoDB e Neo4j."""

from datetime import datetime, timezone

from bson import json_util
from config import MONGODB_DATABASE, NEO4J_DATABASE
from database.mongodb import check_connection as check_mongodb
from database.mongodb import get_client as get_mongo_client
from database.neo4j_db import check_connection as check_neo4j
from database.neo4j_db import get_driver
from database.redis_db import check_connection as check_redis
from database.redis_db import get_client as get_redis


GAMES = [
    {
        "_id": "game-001",
        "nome": "Ecos de Arvandor",
        "genero": "RPG",
        "descricao": "Uma aventura de fantasia sobre alianças e escolhas em um reino antigo.",
        "marca": "Aurora Forge",
        "categorias": ["RPG", "Aventura"],
        "imagem_url": "https://images.example.com/gamehub/ecos-de-arvandor.jpg",
        "especificacoes": {"plataformas": ["PC"], "jogadores": "1", "idiomas": ["pt-BR", "en"]},
        "preco": 89.90,
        "ano": 2023,
    },
    {
        "_id": "game-002",
        "nome": "Neon Drift Circuit",
        "genero": "Corrida",
        "descricao": "Corridas noturnas em pistas urbanas com veículos personalizáveis.",
        "marca": "Pixel Harbor",
        "categorias": ["Corrida", "Arcade"],
        "imagem_url": "https://images.example.com/gamehub/neon-drift-circuit.jpg",
        "especificacoes": {"plataformas": ["PC", "Console"], "jogadores": "1-8", "modo_online": True},
        "preco": 59.90,
        "ano": 2022,
    },
    {
        "_id": "game-003",
        "nome": "Bastião das Estrelas",
        "genero": "Estratégia",
        "descricao": "Construa uma colônia espacial e administre recursos em sistemas distantes.",
        "marca": "Aurora Forge",
        "categorias": ["Estratégia", "Simulação"],
        "imagem_url": "https://images.example.com/gamehub/bastiao-das-estrelas.jpg",
        "especificacoes": {"plataformas": ["PC"], "jogadores": "1", "compatibilidade_controle": True},
        "preco": 74.50,
        "ano": 2024,
    },
    {
        "_id": "game-004",
        "nome": "Marés de Cobalto",
        "genero": "Aventura",
        "descricao": "Explore ilhas e ruínas submersas em uma jornada narrativa cooperativa.",
        "marca": "Lume Interactive",
        "categorias": ["Aventura", "Ação"],
        "imagem_url": "https://images.example.com/gamehub/mares-de-cobalto.jpg",
        "especificacoes": {"plataformas": ["PC", "Console"], "jogadores": "1-2", "modo_cooperativo": True},
        "preco": 109.90,
        "ano": 2025,
    },
    {
        "_id": "game-005",
        "nome": "Crônicas do Vale Cinzento",
        "genero": "RPG",
        "descricao": "Reúna um grupo de viajantes e enfrente criaturas em uma região isolada.",
        "marca": "Lume Interactive",
        "categorias": ["RPG", "Estratégia"],
        "imagem_url": "https://images.example.com/gamehub/cronicas-do-vale-cinzento.jpg",
        "especificacoes": {"plataformas": ["PC"], "jogadores": "1", "classificacao": "12+"},
        "preco": 99.00,
        "ano": 2021,
    },
    {
        "_id": "game-006",
        "nome": "Oficina do Pequeno Cometa",
        "genero": "Puzzle",
        "descricao": "Resolva desafios de lógica para reparar uma estação de pesquisa orbital.",
        "marca": "Pixel Harbor",
        "categorias": ["Puzzle", "Casual"],
        "imagem_url": "https://images.example.com/gamehub/oficina-do-pequeno-cometa.jpg",
        "especificacoes": {"plataformas": ["PC", "Console"], "jogadores": "1", "acessibilidade": ["legendas", "modo daltônico"]},
        "preco": 34.90,
        "ano": 2024,
    },
]

CLIENTS = [
    {"_id": "customer-001", "nome": "Lia Monteiro", "email": "lia.monteiro@example.com"},
    {"_id": "customer-002", "nome": "Caio Nascimento", "email": "caio.nascimento@example.com"},
    {"_id": "customer-003", "nome": "Nina Carvalho", "email": "nina.carvalho@example.com"},
]

HISTORIC_ORDERS = [
    {
        "_id": "seed-order-001",
        "checkout_id": "seed-checkout-001",
        "cliente_id": "customer-001",
        "data_criacao": datetime(2025, 10, 4, 14, 30, tzinfo=timezone.utc),
        "status": "CONCLUIDO",
        "itens": [
            {"jogo_id": "game-001", "nome": "Ecos de Arvandor", "quantidade": 1, "preco_unitario": 89.90},
            {"jogo_id": "game-004", "nome": "Marés de Cobalto", "quantidade": 1, "preco_unitario": 109.90},
        ],
        "total": 199.80,
    },
    {
        "_id": "seed-order-002",
        "checkout_id": "seed-checkout-002",
        "cliente_id": "customer-002",
        "data_criacao": datetime(2025, 11, 12, 18, 0, tzinfo=timezone.utc),
        "status": "CONCLUIDO",
        "itens": [
            {"jogo_id": "game-001", "nome": "Ecos de Arvandor", "quantidade": 1, "preco_unitario": 89.90},
            {"jogo_id": "game-005", "nome": "Crônicas do Vale Cinzento", "quantidade": 1, "preco_unitario": 99.00},
        ],
        "total": 188.90,
    },
    {
        "_id": "seed-order-003",
        "checkout_id": "seed-checkout-003",
        "cliente_id": "customer-003",
        "data_criacao": datetime(2025, 12, 2, 11, 15, tzinfo=timezone.utc),
        "status": "CONCLUIDO",
        "itens": [
            {"jogo_id": "game-001", "nome": "Ecos de Arvandor", "quantidade": 1, "preco_unitario": 89.90},
            {"jogo_id": "game-003", "nome": "Bastião das Estrelas", "quantidade": 1, "preco_unitario": 74.50},
        ],
        "total": 164.40,
    },
    {
        "_id": "seed-order-004",
        "checkout_id": "seed-checkout-004",
        "cliente_id": "customer-002",
        "data_criacao": datetime(2026, 1, 9, 16, 45, tzinfo=timezone.utc),
        "status": "CONCLUIDO",
        "itens": [
            {"jogo_id": "game-002", "nome": "Neon Drift Circuit", "quantidade": 1, "preco_unitario": 59.90},
            {"jogo_id": "game-006", "nome": "Oficina do Pequeno Cometa", "quantidade": 1, "preco_unitario": 34.90},
        ],
        "total": 94.80,
    },
]

RATINGS = [
    {"cliente_id": "customer-001", "jogo_id": "game-001", "nota": 5},
    {"cliente_id": "customer-001", "jogo_id": "game-004", "nota": 4},
    {"cliente_id": "customer-002", "jogo_id": "game-001", "nota": 4},
    {"cliente_id": "customer-002", "jogo_id": "game-005", "nota": 5},
    {"cliente_id": "customer-002", "jogo_id": "game-002", "nota": 3},
    {"cliente_id": "customer-003", "jogo_id": "game-001", "nota": 5},
    {"cliente_id": "customer-003", "jogo_id": "game-003", "nota": 4},
]


def load_mongodb() -> dict[str, int]:
    """Cria índices e grava documentos de demonstração por ID estável."""
    database = get_mongo_client()[MONGODB_DATABASE]

    database.jogos.create_index("nome")
    database.pedidos.create_index("checkout_id", unique=True)

    for game in GAMES:
        database.jogos.replace_one({"_id": game["_id"]}, game, upsert=True)
    for client in CLIENTS:
        database.clientes.replace_one({"_id": client["_id"]}, client, upsert=True)
    for order in HISTORIC_ORDERS:
        database.pedidos.replace_one({"_id": order["_id"]}, order, upsert=True)

    return {
        "jogos": database.jogos.count_documents({}),
        "clientes": database.clientes.count_documents({}),
        "pedidos": database.pedidos.count_documents({}),
    }


def load_neo4j() -> dict[str, int]:
    """Cria o grafo com MERGE e restrições para permitir reexecução."""
    driver = get_driver()
    with driver.session(database=NEO4J_DATABASE) as session:
        constraints = (
            "CREATE CONSTRAINT cliente_id_unico IF NOT EXISTS FOR (n:Cliente) REQUIRE n.id IS UNIQUE",
            "CREATE CONSTRAINT produto_id_unico IF NOT EXISTS FOR (n:Produto) REQUIRE n.id IS UNIQUE",
            "CREATE CONSTRAINT categoria_nome_unico IF NOT EXISTS FOR (n:Categoria) REQUIRE n.nome IS UNIQUE",
        )
        for statement in constraints:
            session.run(statement).consume()

        session.run(
            """
            UNWIND $clients AS client
            MERGE (c:Cliente {id: client.id})
            SET c.nome = client.nome
            """,
            clients=[{"id": c["_id"], "nome": c["nome"]} for c in CLIENTS],
        ).consume()

        session.run(
            """
            UNWIND $games AS game
            MERGE (p:Produto {id: game.id})
            SET p.nome = game.nome, p.preco = game.preco
            WITH p, game
            UNWIND game.categorias AS category_name
            MERGE (category:Categoria {nome: category_name})
            MERGE (p)-[:PERTENCE_A]->(category)
            """,
            games=[
                {"id": g["_id"], "nome": g["nome"], "preco": g["preco"], "categorias": g["categorias"]}
                for g in GAMES
            ],
        ).consume()

        session.run(
            """
            UNWIND $orders AS order
            MATCH (c:Cliente {id: order.cliente_id})
            UNWIND order.itens AS item
            MATCH (p:Produto {id: item.jogo_id})
            MERGE (c)-[r:COMPROU {checkout_id: order.checkout_id}]->(p)
            SET r.data = order.data
            """,
            orders=[
                {
                    "cliente_id": order["cliente_id"],
                    "checkout_id": order["checkout_id"],
                    "data": order["data_criacao"].isoformat(),
                    "itens": order["itens"],
                }
                for order in HISTORIC_ORDERS
            ],
        ).consume()

        session.run(
            """
            UNWIND $ratings AS rating
            MATCH (c:Cliente {id: rating.cliente_id})
            MATCH (p:Produto {id: rating.jogo_id})
            MERGE (c)-[r:AVALIOU]->(p)
            SET r.nota = rating.nota
            """,
            ratings=RATINGS,
        ).consume()

        result = session.run(
            """
            RETURN
              COUNT { (:Cliente) } AS clientes,
              COUNT { (:Produto) } AS produtos,
              COUNT { (:Categoria) } AS categorias,
              COUNT { ()-[:PERTENCE_A]->() } AS pertence_a,
              COUNT { ()-[:COMPROU]->() } AS comprou,
              COUNT { ()-[:AVALIOU]->() } AS avaliou
            """
        ).single()
        return dict(result)


def load_redis_cache() -> int:
    """Preenche somente o cache com documentos reais do catálogo."""
    cache = get_redis()
    games = get_mongo_client()[MONGODB_DATABASE].jogos.find()
    count = 0
    for game in games:
        cache.set(f"gamehub:produto:{game['_id']}", json_util.dumps(game), ex=60)
        count += 1
    return count


def main() -> None:
    """Executa a carga sem acessar ou preencher o Redis."""
    checks = (("MongoDB", check_mongodb), ("Redis", check_redis), ("Neo4j", check_neo4j))
    failed = False
    for name, check in checks:
        try:
            check()
            print(f"[OK] {name}: conexão confirmada.")
        except Exception as error:
            failed = True
            print(f"[FALHA] {name}: {type(error).__name__}; nenhuma carga foi iniciada.")
    if failed:
        raise SystemExit(1)

    mongo_counts = load_mongodb()
    graph_counts = load_neo4j()
    cached_products = load_redis_cache()

    print("Seed concluído.")
    print(
        "MongoDB: "
        f"{mongo_counts['jogos']} jogos, "
        f"{mongo_counts['clientes']} clientes, "
        f"{mongo_counts['pedidos']} pedidos."
    )
    print(
        "Neo4j: "
        f"{graph_counts['produtos']} produtos, "
        f"{graph_counts['clientes']} clientes, "
        f"{graph_counts['categorias']} categorias, "
        f"{graph_counts['pertence_a']} PERTENCE_A, "
        f"{graph_counts['comprou']} COMPROU, "
        f"{graph_counts['avaliou']} AVALIOU."
    )
    print(f"Redis: {cached_products} produtos no cache inicial, TTL de 60 segundos; nenhum carrinho ou token criado.")


if __name__ == "__main__":
    main()
