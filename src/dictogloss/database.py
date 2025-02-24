from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from dictogloss.settings import get_settings


def async_get_db():
    async_engine = create_async_engine(get_settings().DB_DSN)
    async_session = async_sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
