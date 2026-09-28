from pydantic import BaseModel
from typing import List, Optional


# --- Schemas pour les Catégories & Technologies ---
class CategoryResponse(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True


class TechnologyResponse(BaseModel):
    id: str
    name: str
    icon: Optional[str] = None

    class Config:
        from_attributes = True


# --- Schemas pour les Projets ---
class ProjectCreate(BaseModel):
    title: str
    description: str
    image_url: str
    github_url: Optional[str] = None
    demo_url: Optional[str] = None
    project_category_id: str


class ProjectResponse(BaseModel):
    id: str
    title: str
    description: str
    image_url: str
    github_url: Optional[str] = None
    demo_url: Optional[str] = None
    status: str
    category: CategoryResponse
    technologies: List[TechnologyResponse] = []

    class Config:
        from_attributes = True


# --- Schemas pour les Compétences ---
class SkillResponse(BaseModel):
    id: str
    name: str
    level: int
    display_order: int
    category: CategoryResponse

    class Config:
        from_attributes = True