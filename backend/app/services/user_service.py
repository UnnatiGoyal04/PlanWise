from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.exceptions.base import AppException
from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserLogin,
)

async def register_user(
    user_data: UserCreate,
    db: AsyncSession,
) -> User:
    email = user_data.email.strip().lower()
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()
    if existing_user is not None:
        raise AppException(
            status_code=409,
            message="Email is already registered."
        )
    hashed_password = hash_password(
        user_data.password
    )
    user = User(
        name=user_data.name,
        email=email,
        hashed_password=hashed_password,
    )
    try:
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    except Exception:
        await db.rollback()
        raise

async def login_user(
    user_data: UserLogin,
    db: AsyncSession,
) -> dict:
    email = user_data.email.strip().lower()
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    if user is None:
        raise AppException(
            status_code=401,
            message="Invalid email or password."
        )
    if not verify_password(
        user_data.password,
        user.hashed_password,
    ):
        raise AppException(
            status_code=401,
            message="Invalid email or password."
        )
    access_token = create_access_token(
        subject=str(user.id)
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }