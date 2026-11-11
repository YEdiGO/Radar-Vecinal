from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.Repositories.models import Barrio


class BarrioRepository:
    def __init__(self, db: Session):
        self.db = db

    def todos(self) -> list[Barrio]:
        return list(self.db.scalars(select(Barrio).order_by(Barrio.nombre)).all())

    def por_id(self, id_: str) -> Barrio | None:
        return self.db.get(Barrio, id_)