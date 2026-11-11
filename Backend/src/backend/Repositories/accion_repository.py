from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.Repositories.models import AccionMunicipal


class AccionRepository:
    def __init__(self, db: Session):
        self.db = db

    def crear(self, **datos) -> AccionMunicipal:
        accion = AccionMunicipal(**datos)
        self.db.add(accion)
        self.db.commit()
        self.db.refresh(accion)
        return accion

    def por_id(self, id_: int) -> AccionMunicipal | None:
        return self.db.get(AccionMunicipal, id_)

    def listar(
        self, id_barrio: str | None = None, id_autoridad: int | None = None
    ) -> list[AccionMunicipal]:
        stmt = select(AccionMunicipal).order_by(AccionMunicipal.fecha_registro.desc())
        if id_barrio:
            stmt = stmt.where(AccionMunicipal.id_barrio == id_barrio)
        if id_autoridad:
            stmt = stmt.where(AccionMunicipal.id_autoridad == id_autoridad)
        return list(self.db.scalars(stmt).all())

    def barrios_con_accion_desde(self, desde: datetime) -> set[str]:
        stmt = select(AccionMunicipal.id_barrio).where(AccionMunicipal.fecha_registro >= desde)
        return set(self.db.scalars(stmt).all())

    def guardar(self, accion: AccionMunicipal) -> AccionMunicipal:
        self.db.commit()
        self.db.refresh(accion)
        return accion