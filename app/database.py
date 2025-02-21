from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
from app.core.config import settings
from sqlalchemy import MetaData

DATABASE_URL = settings.generate_database_url()
Base = declarative_base()
metadata = MetaData()

engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)  # Ensure connection is alive
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

