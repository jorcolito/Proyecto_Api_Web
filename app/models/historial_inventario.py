from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class TipoMovimiento(str, Enum):
    ENTRADA = "entrada"
    SALIDA = "salida"


class MovimientoInventarioCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    id_producto: int = Field(gt=0)
    id_usuario: int = Field(gt=0)
    tipo_movimiento: TipoMovimiento
    cantidad: int = Field(gt=0)
    motivo: str = Field(min_length=1, max_length=300)
