from typing import Dict, Optional
from sqlmodel import Session
from sqlalchemy.exc import NoResultFound
from domain.entities import (
    VeiculoCreate,
    VeiculoDetail,
    VeiculoList,
    VeiculoPartialUpdate,
    VeiculoUpdate,
)
from domain.exceptions import VEICULO_NOT_FOUND_ERROR, NotFoundError
from models.veiculo import Veiculo
from repositories.veiculo import VeiculoRepository


class VeiculoService:
    def __init__(self, db_session: Session):
        self.veiculo_repository = VeiculoRepository(session=db_session)

    def add(self, veiculo: VeiculoCreate) -> VeiculoDetail:
        veiculo_model = Veiculo(
            veiculo=veiculo.veiculo,
            marca=veiculo.marca,
            ano=veiculo.ano,
            descricao=veiculo.descricao,
            vendido=veiculo.vendido,
        )
        self.veiculo_repository.add(veiculo_model)
        return VeiculoDetail(
            id=veiculo_model.id,
            veiculo=veiculo_model.veiculo,
            marca=veiculo_model.marca,
            ano=veiculo_model.ano,
            descricao=veiculo_model.descricao,
            vendido=veiculo_model.vendido,
            created=veiculo_model.created,
            updated=veiculo_model.updated,
        )

    def get(
        self,
        page: int = 1,
        size: int = 20,
        filters: Optional[Dict[str, str | int | list | bool]] = None,
    ) -> tuple[list[VeiculoList], int]:
        result = self.veiculo_repository.get(page, size, filters)
        veiculos = [
            VeiculoList(
                id=veiculo.id,
                veiculo=veiculo.veiculo,
                marca=veiculo.marca,
                ano=veiculo.ano,
            )
            for veiculo in result[0]
        ]
        total = result[1]
        return veiculos, total

    def update(
        self,
        id: int,
        veiculo: VeiculoUpdate | VeiculoPartialUpdate,
        patch: bool = False,
    ) -> VeiculoDetail:
        try:
            veiculo_model = self.veiculo_repository.update(id, veiculo, patch)
            return VeiculoDetail(
                id=veiculo_model.id,
                veiculo=veiculo_model.veiculo,
                marca=veiculo_model.marca,
                ano=veiculo_model.ano,
                descricao=veiculo_model.descricao,
                vendido=veiculo_model.vendido,
                created=veiculo_model.created,
                updated=veiculo_model.updated,
            )
        except NoResultFound:
            raise NotFoundError(
                f"Veículo com ID {id} não encontrado.",
                code=VEICULO_NOT_FOUND_ERROR,
                status_code=404,
            )

    def delete(self, id: int) -> None:
        try:
            self.veiculo_repository.delete(id)
        except NoResultFound:
            raise NotFoundError(
                f"Veículo com ID {id} não encontrado.",
                code=VEICULO_NOT_FOUND_ERROR,
                status_code=404,
            )

    def get_by_id(self, id: int) -> VeiculoDetail:
        veiculo = self.veiculo_repository.get_by_id(id)
        if veiculo:
            return VeiculoDetail(
                id=veiculo.id,
                veiculo=veiculo.veiculo,
                marca=veiculo.marca,
                ano=veiculo.ano,
                descricao=veiculo.descricao,
                vendido=veiculo.vendido,
                created=veiculo.created,
                updated=veiculo.updated,
            )
        raise NotFoundError(
            f"Veículo com ID {id} não encontrado.",
            code=VEICULO_NOT_FOUND_ERROR,
            status_code=404,
        )
