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
        "nome": "Grand Theft Auto VI",
        "genero": "Ação e aventura",
        "descricao": "Uma aventura de mundo aberto ambientada em Vice City e no estado de Leonida.",
        "marca": "Rockstar Games",
        "categorias": ["Ação", "Mundo aberto"],
        "imagem_path": "images/gta-iv.jpg",
        "especificacoes": {"plataformas": ["PlayStation 5", "Xbox Series X|S"], "jogadores": "1"},
        "preco": 89.90,
        "ano": 2026,
    },
    {
        "_id": "game-002",
        "nome": "Hollow Knight",
        "genero": "Metroidvania",
        "descricao": "Explore Hallownest, um reino subterrâneo interconectado habitado por criaturas e mistérios.",
        "marca": "Team Cherry",
        "categorias": ["Ação", "Aventura", "Metroidvania"],
        "imagem_path": "images/hollow-knight.jpg",
        "especificacoes": {"plataformas": ["PC", "Nintendo Switch", "PlayStation", "Xbox"], "jogadores": "1"},
        "preco": 59.90,
        "ano": 2017,
    },
    {
        "_id": "game-003",
        "nome": "Minecraft",
        "genero": "Sandbox",
        "descricao": "Explore um mundo aberto, reúna recursos e construa no modo Sobrevivência ou Criativo.",
        "marca": "Mojang Studios",
        "categorias": ["Aventura", "Sandbox", "Sobrevivência"],
        "imagem_path": "images/minecraft.jpeg",
        "especificacoes": {"plataformas": ["PC", "Console", "Dispositivos móveis"], "jogadores": "Solo ou multiplayer"},
        "preco": 74.50,
        "ano": 2011,
    },
    {
        "_id": "game-004",
        "nome": "DOOM",
        "genero": "FPS",
        "descricao": "O clássico jogo de tiro em primeira pessoa da id Software, lançado originalmente em 1993.",
        "marca": "id Software",
        "categorias": ["Ação", "Clássico", "FPS"],
        "imagem_path": "images/Doom_cover_art.jpg",
        "especificacoes": {"plataformas": ["PC"], "jogadores": "Solo e multiplayer"},
        "preco": 109.90,
        "ano": 1993,
    },
    {
        "_id": "game-005",
        "nome": "Ori and the Blind Forest: Definitive Edition",
        "genero": "Plataforma",
        "descricao": "Uma aventura de plataforma sobre Ori, um espírito guardião que explora a floresta de Nibel.",
        "marca": "Moon Studios",
        "categorias": ["Aventura", "Plataforma"],
        "imagem_path": "images/ori.jpg",
        "especificacoes": {"plataformas": ["PC", "Xbox", "Nintendo Switch"], "jogadores": "1"},
        "preco": 99.00,
        "ano": 2016,
    },
    {
        "_id": "game-006",
        "nome": "Hollow Knight: Silksong",
        "genero": "Metroidvania",
        "descricao": "Acompanhe Hornet em uma aventura por um reino desconhecido repleto de criaturas e desafios.",
        "marca": "Team Cherry",
        "categorias": ["Ação", "Aventura", "Metroidvania"],
        "imagem_path": "images/silksong.webp",
        "especificacoes": {"plataformas": ["PC", "Nintendo Switch", "PlayStation", "Xbox"], "jogadores": "1"},
        "preco": 34.90,
        "ano": 2025,
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
            {"jogo_id": "game-002", "nome": "Hollow Knight", "quantidade": 1, "preco_unitario": 59.90},
            {"jogo_id": "game-004", "nome": "DOOM", "quantidade": 1, "preco_unitario": 109.90},
        ],
        "total": 169.80,
    },
    {
        "_id": "seed-order-002",
        "checkout_id": "seed-checkout-002",
        "cliente_id": "customer-002",
        "data_criacao": datetime(2025, 11, 12, 18, 0, tzinfo=timezone.utc),
        "status": "CONCLUIDO",
        "itens": [
            {"jogo_id": "game-002", "nome": "Hollow Knight", "quantidade": 1, "preco_unitario": 59.90},
            {"jogo_id": "game-006", "nome": "Hollow Knight: Silksong", "quantidade": 1, "preco_unitario": 34.90},
        ],
        "total": 94.80,
    },
    {
        "_id": "seed-order-003",
        "checkout_id": "seed-checkout-003",
        "cliente_id": "customer-003",
        "data_criacao": datetime(2025, 12, 2, 11, 15, tzinfo=timezone.utc),
        "status": "CONCLUIDO",
        "itens": [
            {"jogo_id": "game-002", "nome": "Hollow Knight", "quantidade": 1, "preco_unitario": 59.90},
            {"jogo_id": "game-003", "nome": "Minecraft", "quantidade": 1, "preco_unitario": 74.50},
        ],
        "total": 134.40,
    },
    {
        "_id": "seed-order-004",
        "checkout_id": "seed-checkout-004",
        "cliente_id": "customer-002",
        "data_criacao": datetime(2026, 1, 9, 16, 45, tzinfo=timezone.utc),
        "status": "CONCLUIDO",
        "itens": [
            {"jogo_id": "game-005", "nome": "Ori and the Blind Forest: Definitive Edition", "quantidade": 1, "preco_unitario": 99.00},
            {"jogo_id": "game-004", "nome": "DOOM", "quantidade": 1, "preco_unitario": 109.90},
        ],
        "total": 208.90,
    },
]

RATINGS = [
    {"cliente_id": "customer-001", "jogo_id": "game-002", "nota": 5},
    {"cliente_id": "customer-001", "jogo_id": "game-004", "nota": 4},
    {"cliente_id": "customer-002", "jogo_id": "game-002", "nota": 4},
    {"cliente_id": "customer-002", "jogo_id": "game-006", "nota": 5},
    {"cliente_id": "customer-002", "jogo_id": "game-004", "nota": 3},
    {"cliente_id": "customer-003", "jogo_id": "game-002", "nota": 5},
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
            "MATCH (:Produto)-[r:PERTENCE_A]->(:Categoria) DELETE r"
        ).consume()
        category_names = sorted({name for game in GAMES for name in game["categorias"]})
        session.run(
            """
            MATCH (category:Categoria)
            WHERE NOT category.nome IN $category_names
            DETACH DELETE category
            """,
            category_names=category_names,
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
            MATCH ()-[r:COMPROU]->()
            WHERE r.checkout_id IN $checkout_ids
            DELETE r
            """,
            checkout_ids=[order["checkout_id"] for order in HISTORIC_ORDERS],
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
            MATCH (c:Cliente)-[r:AVALIOU]->()
            WHERE c.id IN $client_ids
            DELETE r
            """,
            client_ids=[client["_id"] for client in CLIENTS],
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
    """Executa a carga dos bancos e popula apenas o cache do catálogo no Redis."""
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
