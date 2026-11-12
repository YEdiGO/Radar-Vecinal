from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

TipoIncidente = Literal[
    "asalto_robo", "pandillaje", "alcohol_drogas",
    "falta_alumbrado", "actividad_sospechosa", "otro",
]
Descripcion = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=280)]


class ReporteCrear(BaseModel):
    lat: float = Field(ge=-90, le=90)
    lng: float = Field(ge=-180, le=180)
    tipo: TipoIncidente
    descripcion: Descripcion


class VotoIn(BaseModel):
    tipo: Literal["confirmo", "incorrecto"]


class EstadoModeracionIn(BaseModel):
    estado: Literal["activo", "falso", "archivado"]


class ReporteOut(BaseModel):
    """El autor nunca se expone; solo `es_mio`."""
    model_config = ConfigDict(from_attributes=True)
    id: int
    lat: float
    lng: float
    id_barrio: str
    barrio_nombre: str
    tipo: str
    gravedad: int
    descripcion: str
    fecha: datetime
    estado: str
    moderado: bool
    confirmaciones: int
    incorrectos: int
    es_mio: bool = False
    mi_voto: str | None = None