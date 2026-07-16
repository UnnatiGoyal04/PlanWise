from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError


async def check_database(session: AsyncSession) -> bool:
    try:
        await session.execute(text("SELECT 1"))
        return True
    except SQLAlchemyError:
        return False