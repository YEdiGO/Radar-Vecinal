from fastapi import APIRouter

from backend.Apis.deps import Db, Muni
from backend.Schemas.accion import EstadisticasOut
from backend.Schemas.zona import ZonaResumen
from backend.Services.municipalidad_service import MunicipalidadService

router = APIRouter(prefix="/municipalidad", tags=["Municipalidad"])


@router.get("/criticos", response_model=list[ZonaResumen])
def criticos(_: Muni, db: Db):
    return MunicipalidadService(db).criticos()


@router.get("/estadisticas", response_model=EstadisticasOut)
def estadisticas(_: Muni, db: Db):
    return MunicipalidadService(db).estadisticas()