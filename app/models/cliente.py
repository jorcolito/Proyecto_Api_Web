from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


EMAIL_PATTERN = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


class ClienteCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    identificacion: str = Field(min_length=5, max_length=30)
    nombre: str = Field(min_length=1, max_length=100)
    apellido: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=5, max_length=254, pattern=EMAIL_PATTERN)
    telefono: Optional[str] = Field(default=None, min_length=7, max_length=30)


class ClienteUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    identificacion: Optional[str] = Field(default=None, min_length=5, max_length=30)
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=100)
    apellido: Optional[str] = Field(default=None, min_length=1, max_length=100)
    email: Optional[str] = Field(
        default=None,
        min_length=5,
        max_length=254,
        pattern=EMAIL_PATTERN,
    )
    telefono: Optional[str] = Field(default=None, min_length=7, max_length=30)
