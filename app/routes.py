from typing import Annotated
from fastapi import Depends, Query
from fastapi.routing import APIRouter
from sqlmodel import Session

from domain.entities import PaginatedResponse, VeiculoCreate, VeiculoDetail, VeiculoList
from services.veiculo import VeiculoService
from database.sqlmodel import get_session


veiculos_router = APIRouter(prefix="/veiculos", tags=["Veículos"])


@veiculos_router.get("/", response_model=PaginatedResponse[VeiculoList])
async def list_veiculos(
    db_session: Annotated[Session, Depends(get_session)],
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1),
) -> PaginatedResponse[VeiculoList]:
    service = VeiculoService(db_session=db_session)
    veiculos = service.get(page=page, size=size)
    paginated_response = PaginatedResponse[VeiculoList](
        items=veiculos[0],
        total=veiculos[1],
        pages=(veiculos[1] + size - 1) // size,
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
