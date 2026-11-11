from fastapi import APIRouter, status

from backend.Apis.deps import Actual, Db
from backend.Schemas.alerta import AlertaCrear, AlertaOut
from backend.Services.alerta_service import AlertaService

router = APIRouter(prefix="/alertas", tags=["Alertas barriales"])


@router.post("", response_model=AlertaOut, status_code=status.HTTP_201_CREATED)
def crear(datos: AlertaCrear, usuario: Actual, db: Db):
    return AlertaService(db).crear(usuario, datos)


@router.get("/activas", response_model=list[AlertaOut])
def activas(_: Actual, db: Db):
    return AlertaService(db).activas()