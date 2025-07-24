from typing import Optional
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field


class Veiculo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    veiculo: str = Field(max_length=100)
    marca: str = Field(max_length=50)
    ano: int = Field()
    descricao: str = Field(max_length=200)
    vendido: bool = Field(default=False)
    created: datetime = Field(default=datetime.now(timezone.utc), nullable=False)
    updated: datetime = Field(nullable=True)
