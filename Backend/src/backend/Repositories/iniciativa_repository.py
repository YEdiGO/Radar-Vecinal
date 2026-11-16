from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.Repositories.models import Iniciativa, Participacion


class IniciativaRepository:
    def __init__(self, db: Session):
        self.db = db

    def crear(self, **datos) -> Iniciativa:
        ini = Iniciativa(**datos)
        self.db.add(ini)
        self.db.commit()
        self.db.refresh(ini)
        return ini

    def por_id(self, id_: int) -> Iniciativa | None:
        return self.db.get(Iniciativa, id_)

    def listar(self, id_barrio: str | None = None) -> list[Iniciativa]:
        stmt = select(Iniciativa).order_by(Iniciativa.fecha.desc())
        if id_barrio:
            stmt = stmt.where(Iniciativa.id_barrio == id_barrio)
        return list(self.db.scalars(stmt).all())

    def alternar_participacion(self, ini: Iniciativa, id_usuario: int) -> None:
        existente = self.db.get(Participacion, (ini.id, id_usuario))
        if existente:
            self.db.delete(existente)
        else:
            self.db.add(Participacion(id_iniciativa=ini.id, id_usuario=id_usuario))
        self.db.commit()
        self.db.refresh(ini)

    def guardar(self, ini: Iniciativa) -> Iniciativa:
        self.db.commit()
        self.db.refresh(ini)
        return ini