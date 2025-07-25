from sqlmodel import func, select
from models.veiculo import Veiculo
from .base import BaseRepository


class VeiculoRepository(BaseRepository):
    def add(self, model: Veiculo) -> None:
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)

    def get(self, page: int = 1, size: int = 20) -> tuple[list[Veiculo], int]:
        count = self.session.exec(select(func.count()).select_from(Veiculo)).one()
        limit = size * page
        offset = size * (page - 1)
        statement = select(Veiculo).limit(limit).offset(offset)
        result = self.session.exec(statement)
        return ([veiculo for veiculo in result.all()], count)
