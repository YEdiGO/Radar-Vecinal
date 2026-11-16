from datetime import date, datetime
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, StringConstraints

TipoAccion = Literal[
    "Patrullaje de serenazgo", "Operativo con la policía",
    "Alumbrado", "Campaña de prevención", "Otro",
]
EstadoAccion = Literal["Planificada", "En ejecución", "Completada"]
Texto100 = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)]
Texto400 = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=400)]


class AccionCrear(BaseModel):
    id_barrio: str
    tipo: TipoAccion
    titulo: Texto100
    descripcion: Texto400
    fecha: date
    estado: EstadoAccion = "Planificada"


class AccionEstadoIn(BaseModel):
    estado: EstadoAccion


class AccionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    id_barrio: str
    barrio_nombre: str
    institucion: str
    tipo: str
    titulo: str
    descripcion: str
    fecha: date
    estado: str
    fecha_registro: datetime
    temperatura_al_registrar: float | None
    temperatura_al_completar: float | None


class EstadisticasOut(BaseModel):
    vecinos_registrados: int
    reportes_30d: int
    reportes_falsos_pct: float
    barrios_por_nivel: dict[str, int]
    reportes_por_tipo: dict[str, int]
    acciones_por_estado: dict[str, int]
    iniciativas_por_estado: dict[str, int]
    reduccion_promedio: float | None