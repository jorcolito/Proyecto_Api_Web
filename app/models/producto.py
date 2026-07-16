from decimal import Decimal

from pydantic import BaseModel, Field


class ProductoCreate(BaseModel):
    codigo_barras: str = Field(min_length=1, max_length=100)
    nombre: str = Field(min_length=1, max_length=150)
    descripcion: str | None = None
    precio_venta: Decimal = Field(gt=0)
    stock_actual: int = Field(default=0, ge=0)
    stock_minimo: int = Field(default=0, ge=0)
    estado: bool = True