from typing import Generator
from sqlalchemy.engine import Engine
from sqlmodel import Session, create_engine, SQLModel
from config.settings import get_settings

DATABASE_ENGINE = create_engine(get_settings().database_url, echo=True)


def setup_database() -> Engine:
    SQLModel.metadata.create_all(DATABASE_ENGINE)
    return DATABASE_ENGINE


def get_session() -> Generator[Session]:
    with Session(DATABASE_ENGINE) as session:
        yield session
