from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker
)

from utils.config import DSN


engine = create_async_engine(DSN)
async_session = async_sessionmaker(engine)
