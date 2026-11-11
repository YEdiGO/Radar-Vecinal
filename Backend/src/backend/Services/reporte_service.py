from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from backend.config import settings
from backend.Repositories.barrio_repository import BarrioRepository
from backend.Repositories.models import Reporte, Usuario
from backend.Repositories.reporte_repository import ReporteRepository
from backend.Schemas.reporte import ReporteCrear, ReporteOut
from backend.Services.geo import barrio_del_punto
from backend.Services.temperatura import GRAVEDAD


class ReporteService:
    def __init__(self, db: Session):
        self.repo = ReporteRepository(db)
        self.barrios = BarrioRepository(db)

    def salida(self, r: Reporte, usuario: Usuario) -> ReporteOut:
        voto = next((v.tipo for v in r.votos if v.id_usuario == usuario.id), None)
        return ReporteOut.model_validate(r).model_copy(
            update={"es_mio": r.id_usuario == usuario.id, "mi_voto": voto}
        )

    def crear(self, usuario: Usuario, datos: ReporteCrear) -> ReporteOut:
        barrio = barrio_del_punto(datos.lat, datos.lng, self.barrios.todos())
        if not barrio:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                                "El punto debe estar dentro de un barrio del mapa.")
        desde = datetime.now(timezone.utc) - timedelta(days=1)
        if self.repo.contar_desde(usuario.id, desde) >= settings.max_reportes_dia:
            raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS,
                                f"Máximo {settings.max_reportes_dia} reportes por día.")
        r = self.repo.crear(
            id_usuario=usuario.id, id_barrio=barrio.id, lat=datos.lat, lng=datos.lng,
            tipo=datos.tipo, gravedad=GRAVEDAD[datos.tipo], descripcion=datos.descripcion,
        )
        return self.salida(r, usuario)

    def listar(self, usuario: Usuario, solo_mios: bool, id_barrio: str | None, limite: int) -> list[ReporteOut]:
        rs = self.repo.listar(
            id_barrio=id_barrio,
            id_usuario=usuario.id if solo_mios else None,
            limite=limite,
        )
        return [self.salida(r, usuario) for r in rs]

    def _obtener(self, id_: int) -> Reporte:
        r = self.repo.por_id(id_)
        if not r:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Reporte no encontrado.")
        return r

    def votar(self, usuario: Usuario, id_: int, tipo: str) -> ReporteOut:
        r = self._obtener(id_)
        if r.id_usuario == usuario.id:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "No puedes votar tu propio reporte.")
        self.repo.guardar_voto(r.id, usuario.id, tipo)
        r = self.repo.guardar(self._obtener(id_))
        self._recalcular_estado(r)
        return self.salida(self.repo.guardar(r), usuario)

    @staticmethod
    def _recalcular_estado(r: Reporte) -> None:
        if r.moderado:
            return
        if r.incorrectos >= 3 and r.incorrectos > r.confirmaciones:
            r.estado = "falso"
        elif r.confirmaciones >= 3:
            r.estado = "confirmado"
        else:
            r.estado = "activo"

    def eliminar(self, usuario: Usuario, id_: int) -> None:
        r = self._obtener(id_)
        if r.id_usuario != usuario.id and usuario.rol != "municipalidad":
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Solo puedes eliminar tus reportes.")
        self.repo.eliminar(r)

    def moderar(self, usuario: Usuario, id_: int, estado: str) -> ReporteOut:
        r = self._obtener(id_)
        if estado == "activo":
            r.moderado = False
            self._recalcular_estado(r)
        else:
            r.moderado = True
            r.estado = estado
        return self.salida(self.repo.guardar(r), usuario)