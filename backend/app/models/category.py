import uuid
from typing import List, TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.portfolio import Project, Skill


class ProjectCategory(Base):
    """
    Catégories spécifiques aux Projets (ex: Full Stack, Data Science, AI/ML).
    """
    __tablename__ = "project_categories"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    # Relation 1:N vers les projets (sans delete-orphan pour protéger les projets)
    projects: Mapped[List["Project"]] = relationship(
        "Project",
        back_populates="category"
    )


class SkillCategory(Base):
    """
    Catégories spécifiques aux Compétences (ex: Languages, Frameworks, Tools).
    """
    __tablename__ = "skill_categories"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    # Relation 1:N vers les compétences
    skills: Mapped[List["Skill"]] = relationship(
        "Skill",
        back_populates="category"
    )