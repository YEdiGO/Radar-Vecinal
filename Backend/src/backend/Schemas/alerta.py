from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, StringConstraints

MotivoAlerta = Literal[
    "Asalto en curso / Arrebato", "Robo a vivienda forzada",
    "Violencia o riña callejera", "Accidente / Incendio",
]


class AlertaCrear(BaseModel):
    id_barrio: str
    motivo: MotivoAlerta
    ubicacion: Annotated[str, StringConstraints(strip_whitespace=True, max_length=120)] = ""


class AlertaOut(BaseModel):
    id: int
    id_barrio: str
    barrio_nombre: str
    motivo: str
    ubicacion: str
    inicio: datetime
    expira: datetime
    segundos_restantes: int