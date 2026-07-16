from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class DetalleVentaCreate(BaseModel):
    id_venta: int = Field(gt=0)
    id_producto: int = Field(gt=0)
    cantidad: int = Field(gt=0)
    descuento: Decimal = Field(
        default=Decimal("0.00"),
        ge=0,
        max_digits=10,
        decimal_places=2,
    )


class DetalleVentaUpdate(BaseModel):
    cantidad: Optional[int] = Field(default=None, gt=0)
    descuento: Optional[Decimal] = Field(
        default=None,
        ge=0,
        max_digits=10,
        decimal_places=2,
    )

    @model_validator(mode="after")
    def require_change(self):
        if self.cantidad is None and self.descuento is None:
            raise ValueError("Debe enviar cantidad o descuento")
        return self
