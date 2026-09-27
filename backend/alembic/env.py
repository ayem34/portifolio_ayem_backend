import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# 1. Import de notre configuration Pydantic et de nos modèles SQLAlchemy
from app.core.config import settings
from app.models import Base  # Importe Base et TOUS nos modèles centralisés dans app/models/__init__.py

# Configuration des logs d'Alembic
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 2. On indique à Alembic le schéma de nos modèles SQLAlchemy
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Exécute les migrations en mode 'offline' (sans connexion active à la BDD).
    Génère uniquement les scripts SQL.
    """
    url = settings.get_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """
    Exécute les migrations en mode 'online' sur une connexion établie.
    """
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """
    Crée un moteur asynchrone et exécute les migrations.
    """
    # Injection dynamique de notre URL de BDD depuis Pydantic Settings
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = settings.get_database_url()

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        #  Indique à asyncpg d'annuler le cache des requêtes préparées pour Supavisor/PgBouncer
        connect_args={"prepared_statement_cache_size": 0},
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """
    Point d'entrée pour l'exécution des migrations en mode 'online'.
    """
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()