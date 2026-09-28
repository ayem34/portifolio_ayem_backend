from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db_session as get_db
from app.schemas.portfolio import ProjectResponse, SkillResponse
from app.services.portfolio_service import PortfolioService

router = APIRouter()


@router.get("/projects", response_model=List[ProjectResponse])
async def get_projects(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Récupère la liste de tous les projets actifs."""
    service = PortfolioService(db)
    return await service.get_all_projects(skip=skip, limit=limit)


@router.get("/skills", response_model=List[SkillResponse])
async def get_skills(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Récupère la liste de toutes les compétences actives."""
    service = PortfolioService(db)
    return await service.get_all_skills(skip=skip, limit=limit)


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Masque un projet (Soft Delete)."""
    service = PortfolioService(db)
    success = await service.remove_project(project_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projet non trouvé."
        )
    return None