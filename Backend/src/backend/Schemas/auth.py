from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegistroIn(BaseModel):
    nombre: str = Field(min_length=2, max_length=80)
    correo: EmailStr
    clave: str = Field(min_length=6, max_length=72)
    id_barrio: str


class LoginIn(BaseModel):
    correo: EmailStr
    clave: str = Field(min_length=1, max_length=72)


class UsuarioOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre: str
    correo: str
    rol: Literal["vecino", "municipalidad"]
    id_barrio: str | None
    institucion: str | None
    fecha_registro: datetime


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioOut