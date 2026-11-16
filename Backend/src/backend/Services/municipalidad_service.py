from collections import Counter
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from backend.config import settings
from backend.Repositories.accion_repository import AccionRepository
from backend.Repositories.iniciativa_repository import IniciativaRepository
from backend.Repositories.reporte_repository import ReporteRepository
from backend.Repositories.usuario_repository import UsuarioRepository
from backend.Schemas.accion import EstadisticasOut
from backend.Schemas.zona import ZonaResumen
from backend.Services.zona_service import ZonaService


class MunicipalidadService:
    def __init__(self, db: Session):
        self.zonas = ZonaService(db)
        self.acciones = AccionRepository(db)
        self.iniciativas = IniciativaRepository(db)
        self.reportes = ReporteRepository(db)
        self.usuarios = UsuarioRepository(db)

    def criticos(self) -> list[ZonaResumen]:
        """Barrios naranja/rojo sin acción registrada en los últimos 15 días."""
        desde = datetime.now(timezone.utc) - timedelta(days=settings.dias_sin_accion_critico)
        atendidos = self.acciones.barrios_con_accion_desde(desde)
        zonas = [
            z for z in self.zonas.resumen(30)
            if z.nivel in ("naranja", "rojo") and z.id not in atendidos
        ]
        return sorted(zonas, key=lambda z: z.temperatura, reverse=True)

    def estadisticas(self) -> EstadisticasOut:
        ahora = datetime.now(timezone.utc)
        reportes = self.reportes.listar(desde=ahora - timedelta(days=30))
        falsos = sum(1 for r in reportes if r.estado == "falso")
        acciones = self.acciones.listar()
        reducciones = [
            a.temperatura_al_registrar - a.temperatura_al_completar
            for a in acciones
            if a.estado == "Completada"
            and a.temperatura_al_registrar is not None
            and a.temperatura_al_completar is not None
        ]
        return EstadisticasOut(
            vecinos_registrados=self.usuarios.contar_vecinos(),
            reportes_30d=len(reportes),
            reportes_falsos_pct=round(100 * falsos / len(reportes), 1) if reportes else 0.0,
            barrios_por_nivel=dict(Counter(z.nivel for z in self.zonas.resumen(30))),
            reportes_por_tipo=dict(Counter(r.tipo for r in reportes if r.estado != "falso")),
            acciones_por_estado=dict(Counter(a.estado for a in acciones)),
            iniciativas_por_estado=dict(Counter(i.estado for i in self.iniciativas.listar())),
            reduccion_promedio=round(sum(reducciones) / len(reducciones), 1) if reducciones else None,
        )