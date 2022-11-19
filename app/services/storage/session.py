from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core import settings

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine,
    class_=AsyncSession,
)


@asynccontextmanager
async def get_session():
    """Context manager for session."""
    session = SessionLocal()
    try:
        yield session
    finally:
        await session.close()
