from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from backend.config import settings
from backend.Repositories.alerta_repository import AlertaRepository
from backend.Repositories.barrio_repository import BarrioRepository
from backend.Repositories.models import Alerta, Usuario
from backend.Schemas.alerta import AlertaCrear, AlertaOut


def _salida(a: Alerta, ahora: datetime) -> AlertaOut:
    seg = max(0, int((a.expira - ahora).total_seconds()))
    return AlertaOut(
        id=a.id, id_barrio=a.id_barrio, barrio_nombre=a.barrio_nombre, motivo=a.motivo,
        ubicacion=a.ubicacion, inicio=a.inicio, expira=a.expira, segundos_restantes=seg,
    )


class AlertaService:
    def __init__(self, db: Session):
        self.repo = AlertaRepository(db)
        self.barrios = BarrioRepository(db)

    def crear(self, usuario: Usuario, datos: AlertaCrear) -> AlertaOut:
        if not self.barrios.por_id(datos.id_barrio):
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Barrio no válido.")
        ahora = datetime.now(timezone.utc)
        ultima = self.repo.ultima_de_usuario(usuario.id)
        if ultima and ahora - ultima.inicio < timedelta(minutes=settings.espera_entre_alertas_min):
            raise HTTPException(
                status.HTTP_429_TOO_MANY_REQUESTS,
                f"Espera {settings.espera_entre_alertas_min} minutos entre alertas.",
            )
        alerta = self.repo.crear(
            id_barrio=datos.id_barrio, id_usuario=usuario.id, motivo=datos.motivo,
            ubicacion=datos.ubicacion,
            expira=ahora + timedelta(minutes=settings.duracion_alerta_min),
        )
        return _salida(alerta, ahora)

    def activas(self) -> list[AlertaOut]:
        ahora = datetime.now(timezone.utc)
        return [_salida(a, ahora) for a in self.repo.activas(ahora)]