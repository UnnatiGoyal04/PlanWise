from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.schemas.user import (
    UserCreate,
    UserLogin,
    UserResponse,
)
from app.services.user_service import (
    login_user,
    register_user,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    return await register_user(
        user_data=user_data,
        db=db,
    )
@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
)
async def login(
    user_data: UserLogin,
    db: AsyncSession = Depends(get_db),
):
    return await login_user(
        user_data,
        db,
    )