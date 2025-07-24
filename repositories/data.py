from sqlmodel import create_engine, Session, SQLModel
from sqlmodel.main import SQLModelMetaclass
from config.settings import get_settings

engine = create_engine(get_settings().database_url)
SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


class SQLModelRepository:
    _model: SQLModelMetaclass
    _session: Session

    def __init__(self, session: Session):
        self._session = session

    def add(self):
        self._session.add(self._model)
        self._session.commit()
        self._session.refresh(self._model)
