from typing import Optional
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.admin import AdminRepository
from app.models.admin import Admin

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AdminService:
    """Service gérant la logique métier des administrateurs."""

    def __init__(self, session: AsyncSession):
        self.repository = AdminRepository(session)

    async def authenticate_admin(self, email: str, password: str) -> Optional[Admin]:
        """Vérifie les identifiants d'un administrateur et met à jour last_login."""
        admin = await self.repository.get_by_email(email)
        if not admin:
            return None

        if not pwd_context.verify(password, admin.password_hash):
            return None

        await self.repository.update_last_login(admin.id)
        return admin