from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class AdminLogin(BaseModel):
    """Schema pour la requête de connexion d'un admin."""
    email: EmailStr
    password: str


class AdminResponse(BaseModel):
    """Schema pour la réponse renvoyée au client."""
    id: str
    email: EmailStr
    last_login: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True