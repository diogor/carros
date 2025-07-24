from models.veiculo import Veiculo
from .data import SQLModelRepository


class VeiculoRepository(SQLModelRepository):
    _model = Veiculo
