from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from backend.Repositories.accion_repository import AccionRepository
from backend.Repositories.barrio_repository import BarrioRepository
from backend.Repositories.models import AccionMunicipal, Usuario
from backend.Schemas.accion import AccionCrear
from backend.Services.zona_service import ZonaService


class AccionService:
    def __init__(self, db: Session):
        self.repo = AccionRepository(db)
        self.barrios = BarrioRepository(db)
        self.zonas = ZonaService(db)

    def listar(self, usuario: Usuario, id_barrio: str | None, solo_mias: bool) -> list[AccionMunicipal]:
        return self.repo.listar(id_barrio, usuario.id if solo_mias else None)

    def crear(self, usuario: Usuario, datos: AccionCrear) -> AccionMunicipal:
        if not self.barrios.por_id(datos.id_barrio):
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Barrio no válido.")
        t = self.zonas.temperatura_barrio(datos.id_barrio)
        return self.repo.crear(
            **datos.model_dump(),
            id_autoridad=usuario.id,
            institucion=usuario.institucion or "Municipalidad",
            temperatura_al_registrar=t,
            temperatura_al_completar=t if datos.estado == "Completada" else None,
        )

    def cambiar_estado(self, usuario: Usuario, id_: int, estado: str) -> AccionMunicipal:
        accion = self.repo.por_id(id_)
        if not accion:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Acción no encontrada.")
        if accion.id_autoridad != usuario.id:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Solo puedes editar tus acciones.")
        if accion.estado == "Completada":
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "La acción ya está completada.")
        accion.estado = estado
        if estado == "Completada":
            accion.temperatura_al_completar = self.zonas.temperatura_barrio(accion.id_barrio)
        return self.repo.guardar(accion)