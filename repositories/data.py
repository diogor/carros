from sqlmodel import Session, SQLModel, select
from database.sqlmodel import DATABASE_ENGINE


class SQLModelRepository:
    def add(self, model: SQLModel) -> None:
        with Session(DATABASE_ENGINE) as session:
            session.add(model)
            session.commit()
            session.refresh(model)

    def get_all(self, model: SQLModel) -> list[SQLModel]:
        with Session(DATABASE_ENGINE) as session:
            statement = select(model)
            results = session.exec(statement).all()
            return results
