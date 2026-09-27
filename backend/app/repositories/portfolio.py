from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.portfolio import Project, Skill, Technology


class ProjectRepository(BaseRepository[Project]):
    """Repository spécifique pour les projets."""

    def __init__(self, session: AsyncSession):
        super().__init__(model=Project, session=session)

    async def get_with_relations(self, project_id: str) -> Optional[Project]:
        """Récupère un projet actif avec sa catégorie et ses technologies."""
        result = await self.session.execute(
            select(Project)
            .options(
                selectinload(Project.category),
                selectinload(Project.technologies)
            )
            .where(Project.id == project_id)
            .where(Project.deleted_at.is_(None))
        )
        return result.scalars().first()

    async def get_all_with_relations(self, skip: int = 0, limit: int = 100) -> List[Project]:
        """Récupère tous les projets actifs avec leurs relations."""
        result = await self.session.execute(
            select(Project)
            .options(
                selectinload(Project.category),
                selectinload(Project.technologies)
            )
            .where(Project.deleted_at.is_(None))
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())


class SkillRepository(BaseRepository[Skill]):
    """Repository spécifique pour les compétences."""

    def __init__(self, session: AsyncSession):
        super().__init__(model=Skill, session=session)

    async def get_all_with_category(self, skip: int = 0, limit: int = 100) -> List[Skill]:
        """Récupère toutes les compétences actives avec leur catégorie."""
        result = await self.session.execute(
            select(Skill)
            .options(selectinload(Skill.category))
            .where(Skill.deleted_at.is_(None))
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())