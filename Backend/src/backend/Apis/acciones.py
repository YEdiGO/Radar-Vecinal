from fastapi import APIRouter, status

from backend.Apis.deps import Actual, Db, Muni
from backend.Schemas.accion import AccionCrear, AccionEstadoIn, AccionOut
from backend.Services.accion_service import AccionService

router = APIRouter(prefix="/acciones", tags=["Acciones municipales"])


@router.get("", response_model=list[AccionOut])
def listar(usuario: Actual, db: Db, id_barrio: str | None = None, solo_mias: bool = False):
    return AccionService(db).listar(usuario, id_barrio, solo_mias)


@router.post("", response_model=AccionOut, status_code=status.HTTP_201_CREATED)
def crear(datos: AccionCrear, usuario: Muni, db: Db):
    return AccionService(db).crear(usuario, datos)


@router.patch("/{id_}/estado", response_model=AccionOut)
def estado(id_: int, datos: AccionEstadoIn, usuario: Muni, db: Db):
    return AccionService(db).cambiar_estado(usuario, id_, datos.estado)