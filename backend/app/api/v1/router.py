from fastapi import APIRouter
from app.api.v1.endpoints import admin, portfolio

api_router = APIRouter()

# Inclusion des sous-routeurs avec leurs préfixes et tags Swagger
api_router.include_router(
    admin.router, 
    prefix="/auth", 
    tags=["Authentication"]
)

api_router.include_router(
    portfolio.router, 
    prefix="/portfolio", 
    tags=["Portfolio"]
)