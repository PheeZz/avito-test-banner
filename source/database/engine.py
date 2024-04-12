from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import configuration as cfg

if cfg.MODE == "TEST":
    DATABASE_URL = cfg.TEST_DATABASE_URL
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = cfg.ASYNC_DATABASE_URL
    DATABASE_PARAMS = {}


async_engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)

async_session_factory = async_sessionmaker(async_engine)
