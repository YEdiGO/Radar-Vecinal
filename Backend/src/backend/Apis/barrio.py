from fastapi import APIRouter

from backend.Apis.deps import Db
from backend.Repositories.barrio_repository import BarrioRepository
from backend.Schemas.zona import BarrioOut

router = APIRouter(prefix="/barrios", tags=["Barrios"])


@router.get("", response_model=list[BarrioOut])
def listar(db: Db):
    return BarrioRepository(db).todos()