from fastapi import Query
from fastapi.routing import APIRouter

from domain.entities import PaginatedResponse, VeiculoList
from services.veiculo import VeiculoService


veiculos_router = APIRouter(prefix="/veiculos", tags=["Veículos"])


@veiculos_router.get("/", response_model=PaginatedResponse[VeiculoList])
async def list_veiculos(
    page: int = Query(1, ge=1), size: int = Query(20, ge=1)
) -> PaginatedResponse[VeiculoList]:
    service = VeiculoService()
    veiculos = service.get(page=page, size=size)
    paginated_response = PaginatedResponse[VeiculoList](
        items=veiculos[0],
        total=veiculos[1],
        pages=(veiculos[1] + size - 1) // size,
    )
    return paginated_response
