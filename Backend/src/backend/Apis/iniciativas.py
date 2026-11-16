from fastapi import APIRouter, status

from backend.Apis.deps import Actual, Db, Vecino
from backend.Schemas.iniciativa import IniciativaCrear, IniciativaEstadoIn, IniciativaOut
from backend.Services.iniciativa_service import IniciativaService

router = APIRouter(prefix="/iniciativas", tags=["Iniciativas vecinales"])


@router.get("", response_model=list[IniciativaOut])
def listar(usuario: Actual, db: Db, id_barrio: str | None = None):
    return IniciativaService(db).listar(usuario, id_barrio)


@router.post("", response_model=IniciativaOut, status_code=status.HTTP_201_CREATED)
def crear(datos: IniciativaCrear, usuario: Vecino, db: Db):
    return IniciativaService(db).crear(usuario, datos)


@router.post("/{id_}/participar", response_model=IniciativaOut)
def participar(id_: int, usuario: Vecino, db: Db):
    return IniciativaService(db).participar(usuario, id_)


@router.patch("/{id_}/estado", response_model=IniciativaOut)
def estado(id_: int, datos: IniciativaEstadoIn, usuario: Vecino, db: Db):
    return IniciativaService(db).cambiar_estado(usuario, id_, datos.estado)