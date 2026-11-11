from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.Repositories.models import Usuario


class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def por_id(self, id_: int) -> Usuario | None:
        return self.db.get(Usuario, id_)

    def por_correo(self, correo: str) -> Usuario | None:
        return self.db.scalar(select(Usuario).where(Usuario.correo == correo.lower()))

    def crear(self, **datos) -> Usuario:
        usuario = Usuario(**datos)
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def contar_vecinos(self) -> int:
        return self.db.scalar(
            select(func.count()).select_from(Usuario).where(Usuario.rol == "vecino")
        ) or 0