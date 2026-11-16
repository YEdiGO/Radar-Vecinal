from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.Repositories.models import Reporte, Voto


class ReporteRepository:
    def __init__(self, db: Session):
        self.db = db

    def crear(self, **datos) -> Reporte:
        reporte = Reporte(**datos)
        self.db.add(reporte)
        self.db.commit()
        self.db.refresh(reporte)
        return reporte

    def por_id(self, id_: int) -> Reporte | None:
        return self.db.get(Reporte, id_)

    def listar(
        self,
        desde: datetime | None = None,
        id_barrio: str | None = None,
        id_usuario: int | None = None,
        tipo: str | None = None,
        limite: int | None = None,
    ) -> list[Reporte]:
        stmt = select(Reporte).order_by(Reporte.fecha.desc())
        if desde:
            stmt = stmt.where(Reporte.fecha >= desde)
        if id_barrio:
            stmt = stmt.where(Reporte.id_barrio == id_barrio)
        if id_usuario:
            stmt = stmt.where(Reporte.id_usuario == id_usuario)
        if tipo:
            stmt = stmt.where(Reporte.tipo == tipo)
        if limite:
            stmt = stmt.limit(limite)
        return list(self.db.scalars(stmt).all())

    def contar_desde(self, id_usuario: int, desde: datetime) -> int:
        return self.db.scalar(
            select(func.count())
            .select_from(Reporte)
            .where(Reporte.id_usuario == id_usuario, Reporte.fecha >= desde)
        ) or 0

    def voto_de(self, id_reporte: int, id_usuario: int) -> Voto | None:
        return self.db.scalar(
            select(Voto).where(Voto.id_reporte == id_reporte, Voto.id_usuario == id_usuario)
        )

    def guardar_voto(self, id_reporte: int, id_usuario: int, tipo: str) -> None:
        voto = self.voto_de(id_reporte, id_usuario)
        if voto:
            voto.tipo = tipo
        else:
            self.db.add(Voto(id_reporte=id_reporte, id_usuario=id_usuario, tipo=tipo))
        self.db.commit()

    def guardar(self, reporte: Reporte) -> Reporte:
        self.db.commit()
        self.db.refresh(reporte)
        return reporte

    def eliminar(self, reporte: Reporte) -> None:
        self.db.delete(reporte)
        self.db.commit()