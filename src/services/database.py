import contextlib
from typing import AsyncIterator
import ssl

from fastapi import Depends
from sqlalchemy.ext.asyncio import (AsyncConnection, AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)
from sqlalchemy.orm import declarative_base

from config import settings
import psycopg2

Base = declarative_base()


class DatabaseSessionManager:
    def __init__(self):
        self._engine: AsyncEngine | None = None
        self._sessionmaker: async_sessionmaker | None = None

    def init(self, host: str):
        import sqlalchemy
        RDS_CERT_PATH = settings.CERT_PATH

        # ssl_context = ssl.create_default_context(cafile=RDS_CERT_PATH)
        # ssl_context.verify_mode = ssl.CERT_REQUIRED
        # connect_args = {"ssl": ssl_context}
        # yandex postgres
        # self._engine = create_async_engine(host, poolclass=sqlalchemy.NullPool, connect_args=connect_args)

        # cluster postgres
        self._engine = create_async_engine(host, poolclass=sqlalchemy.NullPool)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    # Used for testing
    async def create_all(self, connection: AsyncConnection):
        await connection.run_sync(Base.metadata.create_all)

    async def drop_all(self, connection: AsyncConnection):
        await connection.run_sync(Base.metadata.drop_all)


sessionmanager = DatabaseSessionManager()
sessionmanager.init(settings.DB_CONFIG)


async def get_db():
    async with sessionmanager.session() as session:
        yield session
