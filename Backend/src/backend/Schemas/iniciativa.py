from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, StringConstraints

Texto100 = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)]
Texto200 = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)]
Texto400 = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=400)]
EstadoIniciativa = Literal["Propuesta", "En curso", "Cumplida", "Cancelada"]


class IniciativaCrear(BaseModel):
    id_barrio: str
    titulo: Texto100
    descripcion: Texto400
    meta: Texto200


class IniciativaEstadoIn(BaseModel):
    estado: EstadoIniciativa


class IniciativaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    id_barrio: str
    barrio_nombre: str
    titulo: str
    descripcion: str
    meta: str
    estado: str
    fecha: datetime
    participantes: int
    temperatura_al_crear: float | None
    temperatura_al_cumplir: float | None
    es_mia: bool = False
    participo: bool = False