from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ProductoCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    codigo_barras: str = Field(min_length=1, max_length=100)
    nombre: str = Field(min_length=1, max_length=150)
    descripcion: Optional[str] = Field(default=None, max_length=500)
    precio_venta: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    stock_actual: int = Field(default=0, ge=0)
    stock_minimo: int = Field(default=0, ge=0)
    estado: bool = True


class ProductoUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    codigo_barras: Optional[str] = Field(default=None, min_length=1, max_length=100)
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=150)
    descripcion: Optional[str] = Field(default=None, max_length=500)
    precio_venta: Optional[Decimal] = Field(
        default=None,
        gt=0,
        max_digits=10,
        decimal_places=2,
    )
    stock_minimo: Optional[int] = Field(default=None, ge=0)
    estado: Optional[bool] = None
