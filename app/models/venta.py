from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class VentaCreate(BaseModel):
    id_cliente: int = Field(gt=0)
    id_usuario: int = Field(gt=0)
    impuestos: Decimal = Field(
        default=Decimal("0.00"),
        ge=0,
        max_digits=12,
        decimal_places=2,
    )


class VentaUpdate(BaseModel):
    id_cliente: Optional[int] = Field(default=None, gt=0)
    id_usuario: Optional[int] = Field(default=None, gt=0)
    impuestos: Optional[Decimal] = Field(
        default=None,
        ge=0,
        max_digits=12,
        decimal_places=2,
    )
