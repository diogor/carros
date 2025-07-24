from fastapi.routing import APIRouter

from domain.entities import PaginatedResponse, VeiculoList
from services.veiculo import VeiculoService


veiculos_router = APIRouter(prefix="/veiculos", tags=["Veículos"])


@veiculos_router.get("/", response_model=PaginatedResponse[VeiculoList])
async def list_veiculos() -> PaginatedResponse[VeiculoList]:
    service = VeiculoService()
    veiculos = service.get_all()
    return veiculos
