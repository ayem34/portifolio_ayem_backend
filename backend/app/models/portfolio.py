from datetime import datetime, timezone
import uuid
from typing import List, Optional, TYPE_CHECKING  # <--- Ajout de TYPE_CHECKING
from sqlalchemy import String, Text, ForeignKey, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

# Importation pour le linter (Pylance) uniquement !
if TYPE_CHECKING:
    from app.models.category import ProjectCategory, SkillCategory


class ProjectTechnology(Base):
    """
    Table de liaison Many-to-Many entre Project et Technology.
    Clé primaire composite : (project_id, technology_id).
    """
    __tablename__ = "project_technologies"

    project_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("projects.id", ondelete="CASCADE"),
        primary_key=True
    )
    technology_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("technologies.id", ondelete="RESTRICT"),
        primary_key=True
    )


class Technology(Base):
    """
    Modèle représentant une Technologie (ex: Python, React, Docker).
    """
    __tablename__ = "technologies"

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
    icon: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None
    )

    projects: Mapped[List["Project"]] = relationship(
        "Project",
        secondary="project_technologies",
        back_populates="technologies"
    )
    

class Project(Base):
    """
    Modèle représentant un Projet du Portfolio.
    """
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    title: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    image_url: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    github_url: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True
    )
    demo_url: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True
    )
    status: Mapped[str] = mapped_column(
        String(20),
        default="PUBLISHED",
        nullable=False,
        index=True
    )
    
    project_category_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("project_categories.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    category: Mapped["ProjectCategory"] = relationship(
        "ProjectCategory",
        back_populates="projects"
    )
    technologies: Mapped[List["Technology"]] = relationship(
        "Technology",
        secondary="project_technologies",
        back_populates="projects"
    )


class Skill(Base):
    """
    Modèle représentant une Compétence (ex: FastAPI, PostgreSQL, Git).
    """
    __tablename__ = "skills"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    level: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    display_order: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        index=True
    )

    skill_category_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("skill_categories.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None
    )

    category: Mapped["SkillCategory"] = relationship(
        "SkillCategory",
        back_populates="skills"
    )