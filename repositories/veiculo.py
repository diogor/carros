from datetime import datetime, timezone
from typing import Dict, Optional, Union
from sqlmodel import func, select
from sqlmodel.sql.expression import Select, SelectOfScalar
from domain.entities import VeiculoPartialUpdate, VeiculoUpdate
from models.veiculo import Veiculo
from .base import BaseRepository


class VeiculoRepository(BaseRepository):
    def __select(
        self, filters: Optional[Dict[str, str | int | list | bool]]
    ) -> Union[Select, SelectOfScalar]:
        statement = select(Veiculo)
        filters = {k: v for k, v in filters.items() if v is not None} if filters else {}
        if filters:
            for key, value in filters.items():
                if isinstance(value, list):
                    statement = statement.where(getattr(Veiculo, key).in_(value))
                else:
                    statement = statement.where(getattr(Veiculo, key) == value)
        return statement

    def add(self, model: Veiculo) -> None:
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)

    def get(
        self,
        page: int = 1,
        size: int = 20,
        filters: Optional[Dict[str, str | int | list]] = None,
    ) -> tuple[list[Veiculo], int]:
        limit = size * page
        offset = size * (page - 1)
        statement = self.__select(filters)

        count = self.session.exec(
            select(func.count()).select_from(statement.alias())
        ).one()

        result = self.session.exec(statement.limit(limit).offset(offset))
        return ([veiculo for veiculo in result.all()], count)

    def update(
        self, id: int, model: VeiculoUpdate | VeiculoPartialUpdate, patch: bool = False
    ) -> Veiculo:
        obj = self.session.exec(select(Veiculo).where(Veiculo.id == id)).one()
        for key, value in model.model_dump(exclude_unset=patch).items():
            setattr(obj, key, value)

        obj.updated = datetime.now(timezone.utc)

        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def get_by_id(self, id: int) -> Veiculo | None:
        statement = select(Veiculo).where(Veiculo.id == id)
        result = self.session.exec(statement)
        return result.one_or_none()
