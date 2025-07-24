from models.veiculo import Veiculo
from repositories.veiculo import VeiculoRepository


class VeiculoService:
    def __init__(self):
        self.veiculo_repository = VeiculoRepository()

    def add(self, veiculo: Veiculo):
        self.veiculo_repository.add(veiculo)

    def get_all(self):
        return self.veiculo_repository.get_all()
