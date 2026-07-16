from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class RolUsuario(str, Enum):
    ADMINISTRADOR = "administrador"
    VENDEDOR = "vendedor"


class UsuarioCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    username: str = Field(
        min_length=3,
        max_length=50,
        pattern=r"^[A-Za-z0-9_.-]+$",
    )
    password: str = Field(min_length=8, max_length=128)
    nombre: str = Field(min_length=1, max_length=150)
    rol: RolUsuario
    activo: bool = True


class UsuarioUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    username: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=50,
        pattern=r"^[A-Za-z0-9_.-]+$",
    )
    password: Optional[str] = Field(default=None, min_length=8, max_length=128)
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=150)
    rol: Optional[RolUsuario] = None
    activo: Optional[bool] = None
