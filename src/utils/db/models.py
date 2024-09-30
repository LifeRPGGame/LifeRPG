import asyncio
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    declarative_base
)
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import (
    MetaData,
    Integer,
    BigInteger,
    Float,
    String,
    Boolean,
    DateTime,
    JSON,
    TEXT,
    UniqueConstraint,
    TIME
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import CheckConstraint


from utils.config import DSN
from utils.logging.logger import logger

meta = MetaData()
Base = declarative_base(metadata=meta)


class UserModel(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    full_name: Mapped[str] = mapped_column(String)
    join_time: Mapped[str] = mapped_column(DateTime(timezone=True))
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)
    welcome_notif_id: Mapped[int] = mapped_column(Integer, default=0)
    feature_notif_id: Mapped[int] = mapped_column(Integer, default=0)

    hearts: Mapped[int] = mapped_column(Integer, default=20)
    power: Mapped[int] = mapped_column(Integer, default=10)
    money: Mapped[float] = mapped_column(Float, default=0)
    level: Mapped[int] = mapped_column(Integer, default=1)
    max_hearts: Mapped[int] = mapped_column(Integer, default=20)
    max_power: Mapped[int] = mapped_column(Integer, default=10)

    __table_args__ = (
        CheckConstraint('hearts >= 0', name='check_hearts_non_negative'),
        CheckConstraint('power >= 0', name='check_power_non_negative'),
        CheckConstraint('money >= 0', name='check_money_positive'),
        CheckConstraint('level >= 1', name='check_level_positive'),
    )


class QuestModel(Base):
    __tablename__ = 'quest'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)
    location_id: Mapped[int] = mapped_column(BigInteger, unique=False)
    user_id: Mapped[int] = mapped_column(BigInteger)
    type: Mapped[str] = mapped_column(String, unique=False)
    name: Mapped[str] = mapped_column(String(50), unique=False)
    benefits: Mapped[str] = mapped_column(String(50), unique=False)


class LocationModel(Base):
    __tablename__ = 'location'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=False)
    name: Mapped[str] = mapped_column(String(50), unique=False)


class ItemModel(Base):
    __tablename__ = 'item'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)
    type: Mapped[str] = mapped_column(String, unique=False)
    name: Mapped[str] = mapped_column(String(20), unique=False)
    description: Mapped[str] = mapped_column(String(200), unique=False)
    price: Mapped[float] = mapped_column(Float, unique=False)

    damage: Mapped[float] = mapped_column(Float, nullable=True)  # for weapons
    heal: Mapped[float] = mapped_column(Float, nullable=True)  # for foods


class InventoryModel(Base):
    __tablename__ = 'inventory'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)
    hash_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=False)
    item_id: Mapped[int] = mapped_column(BigInteger, unique=False)
    is_clothed: Mapped[bool] = mapped_column(Boolean, default=False)  # for clothes
    is_weaponed: Mapped[bool] = mapped_column(Boolean, default=False)  # for weapons


async def init_db():
    try:
        engine = create_async_engine(DSN)
        async with engine.begin() as conn:
            await conn.run_sync(meta.create_all)
    except Exception as e:
        if "already exists" in str(e):
            await logger.info('✅ БД уже существуют')
        else:
            await logger.critical(f'Databases crashed: {e}')
