from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BarrioOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    nombre: str
    poligono: list[list[float]]


class TipoFrecuente(BaseModel):
    tipo: str
    cantidad: int


class ZonaResumen(BaseModel):
    id: str
    nombre: str
    poligono: list[list[float]]
    temperatura: float
    nivel: str  # verde | amarillo | naranja | rojo
    cantidad: int
    tipos_frecuentes: list[TipoFrecuente]
    ultima_actualizacion: datetime


class PuntoCaliente(BaseModel):
    lat: float
    lng: float
    temperatura: float
    cantidad: int
    id_barrio: str