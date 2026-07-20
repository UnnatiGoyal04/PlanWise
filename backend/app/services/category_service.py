from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, UTC

from app.models.category import Category
from app.models.user import User
from app.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
)


class CategoryService:

    @staticmethod
    async def create_category(
        db: AsyncSession,
        category_data: CategoryCreate,
        current_user: User,
    ) -> Category:

        existing_category = await db.scalar(
            select(Category).where(
                Category.user_id == current_user.id,
                Category.name == category_data.name,
                Category.deleted_at.is_(None),
            )
        )

        if existing_category:
            raise ValueError(
                "Category with this name already exists."
            )

        category = Category(
            name=category_data.name,
            user_id=current_user.id,
        )

        db.add(category)
        await db.commit()
        await db.refresh(category)

        return category
    
    @staticmethod
    async def get_categories(
        db: AsyncSession,
        current_user: User,
    ) -> list[Category]:

        result = await db.scalars(
            select(Category)
            .where(
                Category.user_id == current_user.id,
                Category.deleted_at.is_(None),
            )
            .order_by(Category.name)
        )

        return list(result)

    @staticmethod
    async def get_category_by_id(
        db: AsyncSession,
        category_id: int,
        current_user: User,
    ) -> Category | None:

        return await db.scalar(
            select(Category).where(
                Category.id == category_id,
                Category.user_id == current_user.id,
                Category.deleted_at.is_(None),
            )
        )

    @staticmethod
    async def update_category(
        db: AsyncSession,
        category: Category,
        category_data: CategoryUpdate,
        current_user: User,
    ) -> Category:

        existing_category = await db.scalar(
            select(Category).where(
                Category.user_id == current_user.id,
                Category.name == category_data.name,
                Category.id != category.id,
                Category.deleted_at.is_(None),
            )
        )

        if existing_category:
            raise ValueError(
                "Category with this name already exists."
            )

        category.name = category_data.name

        await db.commit()
        await db.refresh(category)

        return category

    @staticmethod
    async def delete_category(
        db: AsyncSession,
        category: Category,
    ) -> None:

        category.deleted_at = datetime.now(UTC)
        await db.commit()