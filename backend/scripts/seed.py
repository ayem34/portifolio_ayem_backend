import asyncio
from passlib.context import CryptContext
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.admin import Admin
from app.models.category import ProjectCategory, SkillCategory
from app.models.portfolio import Technology

# Configuration du hachage de mot de passe (Bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def seed_data():
    """Injecte les données de départ obligatoires dans la base de données."""
    async with AsyncSessionLocal() as session:
        print(" Démarrage du Seeding de la base de données...")

        # 1. Seeding de l'Admin Initial
        admin_email = "marieayemou20@gmail.com"
        result = await session.execute(
            select(Admin).where(Admin.email == admin_email)
        )
        existing_admin = result.scalars().first()

        if not existing_admin:
            hashed_password = pwd_context.hash("AdminJustine&7!")
            new_admin = Admin(
                email=admin_email,
                password_hash=hashed_password,  
            )
            session.add(new_admin)
            print(f" Administrateur créé : {admin_email}")
        else:
            print(f"Administrateur {admin_email} existe déjà.")

        # 2. Seeding des Catégories de Projets
        project_categories = ["Fullstack", "Backend", "Frontend", "Data Science / IA"]
        for cat_name in project_categories:
            res = await session.execute(
                select(ProjectCategory).where(ProjectCategory.name == cat_name)
            )
            if not res.scalars().first():
                session.add(ProjectCategory(name=cat_name))
                print(f" Catégorie de projet ajoutée : {cat_name}")

        # 3. Seeding des Catégories de Compétences
        skill_categories = ["Langages", "Frameworks & Libs", "Bases de données", "DevOps & Cloud"]
        for cat_name in skill_categories:
            res = await session.execute(
                select(SkillCategory).where(SkillCategory.name == cat_name)
            )
            if not res.scalars().first():
                session.add(SkillCategory(name=cat_name))
                print(f" Catégorie de compétence ajoutée : {cat_name}")

        # 4. Seeding des Technologies de base
        techs = ["Python", "FastAPI", "PostgreSQL", "React", "Docker", "Laravel"]
        for tech_name in techs:
            res = await session.execute(
                select(Technology).where(Technology.name == tech_name)
            )
            if not res.scalars().first():
                session.add(Technology(name=tech_name))
                print(f" Technologie ajoutée : {tech_name}")

        # Validation globale de la transaction
        await session.commit()
        print(" Seeding terminé avec succès !")


if __name__ == "__main__":
    asyncio.run(seed_data())