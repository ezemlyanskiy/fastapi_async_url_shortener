from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.ext.declarative import declarative_base

from .config import get_settings

async_engine = create_async_engine(get_settings().db_url, echo=True)

async_session = async_sessionmaker(async_engine, expire_on_commit=False)

Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, Any]:
    async with async_session() as session, session.begin():
        yield session


async def init_models() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
