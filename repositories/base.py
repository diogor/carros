from sqlmodel import Session


class BaseRepository:
    session: Session

    def __init__(self, session: Session):
        self.session = session
