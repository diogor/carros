from typing import Generic, TypeVar
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

M = TypeVar("M")


class PaginatedResponse(GenericModel, Generic[M]):
    total: int
    pages: int
    items: list[M]


class VeiculoList(BaseModel):
    id: int
    veiculo: str = Field(max_length=100)
    marca: str = Field(max_length=50)
    ano: int


class VeiculoDetail(VeiculoList):
    descricao: str = Field(max_length=200)
    vendido: bool
    created: str
    updated: str | None


class VeiculoCreate(BaseModel):
    veiculo: str = Field(max_length=100)
    marca: str = Field(max_length=50)
    ano: int
    descricao: str = Field(max_length=200)
    vendido: bool = False
