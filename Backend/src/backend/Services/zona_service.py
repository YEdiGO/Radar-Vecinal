from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from backend.Repositories.barrio_repository import BarrioRepository
from backend.Repositories.reporte_repository import ReporteRepository
from backend.Schemas.zona import PuntoCaliente, TipoFrecuente, ZonaResumen
from backend.Services.temperatura import nivel, peso_reporte, temperatura

INVALIDOS = ("falso", "archivado")


class ZonaService:
    def __init__(self, db: Session):
        self.barrios = BarrioRepository(db)
        self.reportes = ReporteRepository(db)

    def resumen(self, dias: int = 30, tipo: str | None = None) -> list[ZonaResumen]:
        ahora = datetime.now(timezone.utc)
        reportes = self.reportes.listar(desde=ahora - timedelta(days=dias), tipo=tipo)
        por_barrio: dict[str, list] = defaultdict(list)
        for r in reportes:
            if r.estado not in INVALIDOS:
                por_barrio[r.id_barrio].append(r)

        zonas = []
        for b in self.barrios.todos():
            rs = por_barrio.get(b.id, [])
            t = round(temperatura(rs, ahora), 1)
            conteo = Counter(r.tipo for r in rs)
            zonas.append(ZonaResumen(
                id=b.id, nombre=b.nombre, poligono=b.poligono,
                temperatura=t, nivel=nivel(t), cantidad=len(rs),
                tipos_frecuentes=[TipoFrecuente(tipo=k, cantidad=v) for k, v in conteo.most_common(3)],
                ultima_actualizacion=ahora,
            ))
        return zonas

    def temperatura_barrio(self, id_barrio: str) -> float:
        ahora = datetime.now(timezone.utc)
        rs = self.reportes.listar(desde=ahora - timedelta(days=90), id_barrio=id_barrio)
        return round(temperatura(rs, ahora), 1)

    def puntos_calientes(self, dias: int = 30, limite: int = 10) -> list[PuntoCaliente]:
        ahora = datetime.now(timezone.utc)
        puntos: dict[tuple, dict] = {}
        for r in self.reportes.listar(desde=ahora - timedelta(days=dias)):
            if r.estado in INVALIDOS:
                continue
            clave = (round(r.lat, 3), round(r.lng, 3))
            p = puntos.setdefault(clave, {"lat": clave[0], "lng": clave[1],
                                          "temperatura": 0.0, "cantidad": 0, "id_barrio": r.id_barrio})
            p["temperatura"] += peso_reporte(r, ahora)
            p["cantidad"] += 1
        ordenados = sorted(puntos.values(), key=lambda p: p["temperatura"], reverse=True)[:limite]
        return [PuntoCaliente(**{**p, "temperatura": round(p["temperatura"], 1)}) for p in ordenados]