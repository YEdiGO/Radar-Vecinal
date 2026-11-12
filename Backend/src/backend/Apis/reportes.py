from typing import Annotated

from fastapi import APIRouter, Query, Response, status

from backend.Apis.deps import Actual, Db, Muni, Vecino
from backend.Schemas.reporte import EstadoModeracionIn, ReporteCrear, ReporteOut, VotoIn
from backend.Services.reporte_service import ReporteService

router = APIRouter(prefix="/reportes", tags=["Reportes"])


@router.post("", response_model=ReporteOut, status_code=status.HTTP_201_CREATED)
def crear(datos: ReporteCrear, usuario: Vecino, db: Db):
    return ReporteService(db).crear(usuario, datos)


@router.get("", response_model=list[ReporteOut])
def listar(
    usuario: Actual, db: Db,
    solo_mios: bool = False,
    id_barrio: str | None = None,
    limite: Annotated[int, Query(ge=1, le=200)] = 50,
):
    return ReporteService(db).listar(usuario, solo_mios, id_barrio, limite)


@router.post("/{id_}/voto", response_model=ReporteOut)
def votar(id_: int, datos: VotoIn, usuario: Vecino, db: Db):
    return ReporteService(db).votar(usuario, id_, datos.tipo)


@router.delete("/{id_}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(id_: int, usuario: Actual, db: Db):
    ReporteService(db).eliminar(usuario, id_)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/{id_}/estado", response_model=ReporteOut)
def moderar(id_: int, datos: EstadoModeracionIn, usuario: Muni, db: Db):
    return ReporteService(db).moderar(usuario, id_, datos.estado)