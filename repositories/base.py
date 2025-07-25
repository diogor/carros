from sqlmodel import Session
from database.sqlmodel import setup_database

db = setup_database()


def get_session() -> Session:
    with Session(db) as session:
        return session


class BaseRepository:
    session: Session

    def __init__(self):
        self.session = get_session()
