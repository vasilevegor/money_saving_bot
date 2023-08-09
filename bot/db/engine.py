from typing import Union

import sqlalchemy.ext.asyncio
from sqlalchemy import create_engine, Engine, MetaData
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine


def create_async_engine(url: Union[URL, str]) -> AsyncEngine:
    return _create_async_engine(url=url, echo=True, pool_pre_ping=True)


@DeprecationWarning
async def proceed_schemas(engine: AsyncEngine, metadata: MetaData) -> None:
    # async with engine.begin() as conn:
    #     await conn.run_sync(metadata.create_all)
    ...


def get_session_maker(engine: sqlalchemy.ext.asyncio.AsyncEngine) -> sessionmaker:
    return sessionmaker(engine, class_=sqlalchemy.ext.asyncio.AsyncSession, expire_on_commit=False)


