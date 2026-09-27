from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.portfolio import ProjectRepository, SkillRepository
from app.models.portfolio import Project, Skill


class PortfolioService:
    """Service gérant la logique métier des projets et compétences."""

    def __init__(self, session: AsyncSession):
        self.project_repo = ProjectRepository(session)
        self.skill_repo = SkillRepository(session)

    async def get_all_projects(self, skip: int = 0, limit: int = 100) -> List[Project]:
        """Récupère les projets actifs avec leurs catégories et technologies."""
        return await self.project_repo.get_all_with_relations(skip=skip, limit=limit)

    async def get_all_skills(self, skip: int = 0, limit: int = 100) -> List[Skill]:
        """Récupère les compétences actives avec leur catégorie."""
        return await self.skill_repo.get_all_with_category(skip=skip, limit=limit)

    async def remove_project(self, project_id: str) -> bool:
        """Effectue un Soft Delete sur un projet."""
        return await self.project_repo.soft_delete(project_id)