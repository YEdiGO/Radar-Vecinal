from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from backend.Repositories.barrio_repository import BarrioRepository
from backend.Repositories.iniciativa_repository import IniciativaRepository
from backend.Repositories.models import Iniciativa, Usuario
from backend.Schemas.iniciativa import IniciativaCrear, IniciativaOut
from backend.Services.zona_service import ZonaService


class IniciativaService:
    def __init__(self, db: Session):
        self.repo = IniciativaRepository(db)
        self.barrios = BarrioRepository(db)
        self.zonas = ZonaService(db)

    def salida(self, ini: Iniciativa, usuario: Usuario) -> IniciativaOut:
        return IniciativaOut.model_validate(ini).model_copy(update={
            "es_mia": ini.id_creador == usuario.id,
            "participo": any(p.id_usuario == usuario.id for p in ini.participaciones),
        })

    def _obtener(self, id_: int) -> Iniciativa:
        ini = self.repo.por_id(id_)
        if not ini:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Iniciativa no encontrada.")
        return ini

    def listar(self, usuario: Usuario, id_barrio: str | None) -> list[IniciativaOut]:
        return [self.salida(i, usuario) for i in self.repo.listar(id_barrio)]

    def crear(self, usuario: Usuario, datos: IniciativaCrear) -> IniciativaOut:
        if not self.barrios.por_id(datos.id_barrio):
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Barrio no válido.")
        ini = self.repo.crear(
            **datos.model_dump(),
            id_creador=usuario.id,
            temperatura_al_crear=self.zonas.temperatura_barrio(datos.id_barrio),
        )
        self.repo.alternar_participacion(ini, usuario.id)  # el creador participa
        return self.salida(ini, usuario)

    def participar(self, usuario: Usuario, id_: int) -> IniciativaOut:
        ini = self._obtener(id_)
        if ini.estado in ("Cumplida", "Cancelada"):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "La iniciativa ya está cerrada.")
        self.repo.alternar_participacion(ini, usuario.id)
        return self.salida(ini, usuario)

    def cambiar_estado(self, usuario: Usuario, id_: int, estado: str) -> IniciativaOut:
        ini = self._obtener(id_)
        if ini.id_creador != usuario.id:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Solo el creador cambia el estado.")
        if ini.estado in ("Cumplida", "Cancelada"):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "La iniciativa ya está cerrada.")
        ini.estado = estado
        if estado == "Cumplida" and ini.temperatura_al_cumplir is None:
            ini.temperatura_al_cumplir = self.zonas.temperatura_barrio(ini.id_barrio)
        return self.salida(self.repo.guardar(ini), usuario)