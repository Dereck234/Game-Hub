"""Verifica as conexões com MongoDB, Redis e Neo4j."""

from database.mongodb import check_connection as check_mongodb
from database.neo4j_db import check_connection as check_neo4j
from database.redis_db import check_connection as check_redis


def main() -> int:
    checks = (
        ("MongoDB", check_mongodb),
        ("Redis", check_redis),
        ("Neo4j", check_neo4j),
    )
    failed = False

    for name, check in checks:
        try:
            check()
            print(f"[OK] {name}: conexão confirmada.")
        except Exception as error:
            failed = True
            print(f"[FALHA] {name}: {type(error).__name__}. Confira o .env e o estado do serviço.")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
