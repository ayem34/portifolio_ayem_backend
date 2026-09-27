from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

# 1. Création du moteur asynchrone (l'Engine)
# echo=True permet d'afficher les requêtes SQL générées dans la console en environnement de dev
engine = create_async_engine(
    settings.get_database_url(),
    echo=(settings.ENVIRONMENT == "development"),
    future=True,
    connect_args={"prepared_statement_cache_size": 0},

)

# 2. Fabrique de sessions asynchrones
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


# 3. Base déclarative pour nos modèles ORM
class Base(DeclarativeBase):
    """
    Classe parente pour tous les modèles SQLAlchemy de l'application.
    """

    pass


# 4. Dépendance FastAPI pour obtenir une session par requête HTTP
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Générateur de session de base de données.
    Ouvre une session pour la durée d'une requête HTTP et la ferme automatiquement après.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()