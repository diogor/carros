from typing import Annotated, Optional
from fastapi import Depends, Query
from fastapi.routing import APIRouter
from pydantic import BaseModel
from sqlmodel import Session

from domain.entities import (
    PaginatedResponse,
    VeiculoCreate,
    VeiculoDetail,
    VeiculoList,
    VeiculoUpdate,
)
from services.veiculo import VeiculoService
from database.sqlmodel import get_session


veiculos_router = APIRouter(prefix="/veiculos", tags=["Veículos"])


class FilterQuery(BaseModel):
    model_config = {"extra": "forbid"}

    page: int = Query(1, ge=1)
    size: int = Query(20, ge=1)
    veiculo: str = Query(None)
    marca: str = Query(None)
    ano: int = Query(None)
    descricao: str = Query(None)
    vendido: bool = Query(None)


@veiculos_router.get("/", response_model=PaginatedResponse[VeiculoList])
async def list_veiculos(
    db_session: Annotated[Session, Depends(get_session)],
    query: Annotated[FilterQuery, Query()],
) -> PaginatedResponse[VeiculoList]:
    service = VeiculoService(db_session=db_session)

    veiculos = service.get(
        page=query.page,
        size=query.size,
        filters={
            "veiculo": query.veiculo,
            "marca": query.marca,
            "ano": query.ano,
            "descricao": query.descricao,
            "vendido": query.vendido,
        },
    )

    paginated_response = PaginatedResponse[VeiculoList](
        items=veiculos[0],
        total=veiculos[1],
        pages=(veiculos[1] + query.size - 1) // query.size,
    )

    return paginated_response


@veiculos_router.post("/", response_model=VeiculoDetail)
async def create_veiculo(
    db_session: Annotated[Session, Depends(get_session)], veiculo: VeiculoCreate
) -> VeiculoDetail:
    service = VeiculoService(db_session=db_session)
    return service.add(veiculo)


@veiculos_router.get(
    "/{id}",
    response_model=VeiculoDetail,
    responses={404: {"description": "Veículo não encontrado"}},
)
async def get_veiculo(
    db_session: Annotated[Session, Depends(get_session)], id: int
) -> VeiculoDetail | None:
    service = VeiculoService(db_session=db_session)
    return service.get_by_id(id)


@veiculos_router.put(
    "/{id}",
    response_model=VeiculoDetail,
    responses={404: {"description": "Veículo não encontrado"}},
)
async def update_veiculo(
    db_session: Annotated[Session, Depends(get_session)],
    id: int,
    veiculo: VeiculoUpdate,
) -> VeiculoDetail:
    service = VeiculoService(db_session=db_session)
    return service.update(id, veiculo)
