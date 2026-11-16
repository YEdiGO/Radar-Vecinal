from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.Repositories.models import Alerta


class AlertaRepository:
    def __init__(self, db: Session):
        self.db = db

    def crear(self, **datos) -> Alerta:
        alerta = Alerta(**datos)
        self.db.add(alerta)
        self.db.commit()
        self.db.refresh(alerta)
        return alerta

    def activas(self, ahora: datetime) -> list[Alerta]:
        stmt = select(Alerta).where(Alerta.expira > ahora).order_by(Alerta.inicio.desc())
        return list(self.db.scalars(stmt).all())

    def ultima_de_usuario(self, id_usuario: int) -> Alerta | None:
        stmt = (
            select(Alerta)
            .where(Alerta.id_usuario == id_usuario)
            .order_by(Alerta.inicio.desc())
            .limit(1)
        )
        return self.db.scalar(stmt)