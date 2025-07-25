from sqlalchemy.engine import Engine
from sqlmodel import create_engine, SQLModel
from config.settings import get_settings

DATABASE_ENGINE: Engine | None = None


def setup_database() -> Engine:
    DATABASE_ENGINE = create_engine(get_settings().database_url)
    SQLModel.metadata.create_all(DATABASE_ENGINE)
    return DATABASE_ENGINE
