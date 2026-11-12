from datetime import date, datetime, timezone

from sqlalchemy import (JSON, Boolean, Date, DateTime, Float, ForeignKey,
                        Integer, String, Text, UniqueConstraint)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.Repositories.database import Base


def ahora() -> datetime:
    return datetime.now(timezone.utc)


class Barrio(Base):
    __tablename__ = "barrios"
    id: Mapped[str] = mapped_column(String(20), primary_key=True)
    nombre: Mapped[str] = mapped_column(String(80), unique=True)
    poligono: Mapped[list] = mapped_column(JSON)  # [[lat, lng], ...]


class Usuario(Base):
    __tablename__ = "usuarios"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(80))
    correo: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(100))
    rol: Mapped[str] = mapped_column(String(20))  # vecino | municipalidad
    id_barrio: Mapped[str | None] = mapped_column(ForeignKey("barrios.id"), nullable=True)
    institucion: Mapped[str | None] = mapped_column(String(60), nullable=True)
    fecha_registro: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=ahora)


class Reporte(Base):
    __tablename__ = "reportes"
    id: Mapped[int] = mapped_column(primary_key=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), index=True)
    id_barrio: Mapped[str] = mapped_column(ForeignKey("barrios.id"), index=True)
    lat: Mapped[float] = mapped_column(Float)
    lng: Mapped[float] = mapped_column(Float)
    tipo: Mapped[str] = mapped_column(String(30))
    gravedad: Mapped[int] = mapped_column(Integer)
    descripcion: Mapped[str] = mapped_column(String(280))
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=ahora, index=True)
    estado: Mapped[str] = mapped_column(String(20), default="activo")  # activo|confirmado|falso|archivado
    moderado: Mapped[bool] = mapped_column(Boolean, default=False)

    barrio: Mapped[Barrio] = relationship(lazy="joined")
    votos: Mapped[list["Voto"]] = relationship(cascade="all, delete-orphan", lazy="selectin")

    @property
    def barrio_nombre(self) -> str:
        return self.barrio.nombre

    @property
    def confirmaciones(self) -> int:
        return sum(1 for v in self.votos if v.tipo == "confirmo")

    @property
    def incorrectos(self) -> int:
        return sum(1 for v in self.votos if v.tipo == "incorrecto")


class Voto(Base):
    __tablename__ = "votos"
    __table_args__ = (UniqueConstraint("id_reporte", "id_usuario"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    id_reporte: Mapped[int] = mapped_column(ForeignKey("reportes.id", ondelete="CASCADE"))
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    tipo: Mapped[str] = mapped_column(String(12))  # confirmo | incorrecto


class Iniciativa(Base):
    __tablename__ = "iniciativas"
    id: Mapped[int] = mapped_column(primary_key=True)
    id_barrio: Mapped[str] = mapped_column(ForeignKey("barrios.id"), index=True)
    id_creador: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    titulo: Mapped[str] = mapped_column(String(100))
    descripcion: Mapped[str] = mapped_column(Text)
    meta: Mapped[str] = mapped_column(String(200))
    estado: Mapped[str] = mapped_column(String(20), default="Propuesta")
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=ahora)
    temperatura_al_crear: Mapped[float | None] = mapped_column(Float, nullable=True)
    temperatura_al_cumplir: Mapped[float | None] = mapped_column(Float, nullable=True)

    barrio: Mapped[Barrio] = relationship(lazy="joined")
    participaciones: Mapped[list["Participacion"]] = relationship(
        cascade="all, delete-orphan", lazy="selectin"
    )

    @property
    def barrio_nombre(self) -> str:
        return self.barrio.nombre

    @property
    def participantes(self) -> int:
        return len(self.participaciones)


class Participacion(Base):
    __tablename__ = "participaciones"
    id_iniciativa: Mapped[int] = mapped_column(
        ForeignKey("iniciativas.id", ondelete="CASCADE"), primary_key=True
    )
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), primary_key=True)


class AccionMunicipal(Base):
    __tablename__ = "acciones"
    id: Mapped[int] = mapped_column(primary_key=True)
    id_barrio: Mapped[str] = mapped_column(ForeignKey("barrios.id"), index=True)
    id_autoridad: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    institucion: Mapped[str] = mapped_column(String(60))
    tipo: Mapped[str] = mapped_column(String(40))
    titulo: Mapped[str] = mapped_column(String(100))
    descripcion: Mapped[str] = mapped_column(Text)
    fecha: Mapped[date] = mapped_column(Date)
    estado: Mapped[str] = mapped_column(String(20), default="Planificada")
    fecha_registro: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=ahora)
    temperatura_al_registrar: Mapped[float | None] = mapped_column(Float, nullable=True)
    temperatura_al_completar: Mapped[float | None] = mapped_column(Float, nullable=True)

    barrio: Mapped[Barrio] = relationship(lazy="joined")

    @property
    def barrio_nombre(self) -> str:
        return self.barrio.nombre


class Alerta(Base):
    __tablename__ = "alertas"
    id: Mapped[int] = mapped_column(primary_key=True)
    id_barrio: Mapped[str] = mapped_column(ForeignKey("barrios.id"), index=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    motivo: Mapped[str] = mapped_column(String(40))
    ubicacion: Mapped[str] = mapped_column(String(120), default="")
    inicio: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=ahora)
    expira: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    barrio: Mapped[Barrio] = relationship(lazy="joined")

    @property
    def barrio_nombre(self) -> str:
        return self.barrio.nombre