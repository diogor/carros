from datetime import datetime
from typing import Generic, Optional, TypeVar
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

M = TypeVar("M")


class PaginatedResponse(GenericModel, Generic[M]):
    total: int
    pages: int
    items: list[M]


class VeiculoList(BaseModel):
    id: Optional[int]
    veiculo: str = Field(max_length=100)
    marca: str = Field(max_length=50)
    ano: int


class VeiculoDetail(VeiculoList):
    descricao: str = Field(max_length=200)
    vendido: bool
    created: datetime | None
    updated: datetime | None


class VeiculoCreate(BaseModel):
    veiculo: str = Field(max_length=100)
    marca: str = Field(max_length=50)
    ano: int
    descricao: str = Field(max_length=200)
    vendido: bool = False


class VeiculoUpdate(BaseModel):
    descricao: str = Field(max_length=200)
    vendido: bool
    veiculo: str = Field(max_length=100)
    marca: str = Field(max_length=50)
    ano: int


class VeiculoPartialUpdate(BaseModel):
    descricao: Optional[str] = Field(max_length=200, default=None)
    vendido: Optional[bool] = None
    veiculo: Optional[str] = Field(max_length=100, default=None)
    marca: Optional[str] = Field(max_length=50, default=None)
    ano: Optional[int] = None
