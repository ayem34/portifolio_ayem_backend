from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.admin import Admin


class AdminRepository(BaseRepository[Admin]):
    """Repository spécifique pour la gestion du modèle Admin."""

    def __init__(self, session: AsyncSession):
        super().__init__(model=Admin, session=session)

    async def get_by_email(self, email: str) -> Optional[Admin]:
        """Récupère un administrateur actif par son email."""
        result = await self.session.execute(
            select(Admin)
            .where(Admin.email == email)
            .where(Admin.deleted_at.is_(None))
        )
        return result.scalars().first()

    async def update_last_login(self, admin_id: str) -> None:
        """Met à jour le champ last_login lors d'une connexion réussie."""
        await self.session.execute(
            update(Admin)
            .where(Admin.id == admin_id)
            .values(last_login=datetime.now(timezone.utc))
        )
        await self.session.commit()