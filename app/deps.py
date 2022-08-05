from sqlalchemy.ext.asyncio import AsyncSession

from app.config import async_session


async def get_db() -> AsyncSession:
    """Yields db sessions"""
    async with async_session() as session:
        yield session
        await session.commit()
