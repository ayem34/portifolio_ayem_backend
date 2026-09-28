from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db_session as get_db
from app.schemas.admin import AdminLogin, AdminResponse
from app.services.admin_service import AdminService

router = APIRouter()


@router.post("/login", response_model=AdminResponse)
async def login(
    credentials: AdminLogin,
    db: AsyncSession = Depends(get_db)
):
    """Endpoint de connexion de l'administrateur."""
    service = AdminService(db)
    admin = await service.authenticate_admin(
        email=credentials.email,
        password=credentials.password
    )
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect."
        )
    return admin