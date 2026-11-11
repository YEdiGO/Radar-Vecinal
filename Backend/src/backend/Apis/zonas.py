from typing import Annotated

from fastapi import APIRouter, Query

from backend.Apis.deps import Actual, Db
from backend.Schemas.reporte import TipoIncidente
from backend.Schemas.zona import PuntoCaliente, ZonaResumen
from backend.Services.zona_service import ZonaService

router = APIRouter(prefix="/zonas", tags=["Mapa de calor"])


@router.get("", response_model=list[ZonaResumen])
def zonas(
    _: Actual, db: Db,
    dias: Annotated[int, Query(ge=1, le=90)] = 30,
    tipo: TipoIncidente | None = None,
):
    return ZonaService(db).resumen(dias, tipo)


@router.get("/puntos-calientes", response_model=list[PuntoCaliente])
def puntos_calientes(_: Actual, db: Db, dias: Annotated[int, Query(ge=1, le=90)] = 30):
    return ZonaService(db).puntos_calientes(dias)