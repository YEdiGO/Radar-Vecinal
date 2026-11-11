from datetime import datetime, timezone

from backend.config import settings
from backend.Repositories.models import Reporte

GRAVEDAD = {
    "asalto_robo": 5,
    "pandillaje": 3,
    "alcohol_drogas": 3,
    "falta_alumbrado": 2,
    "actividad_sospechosa": 1,
    "otro": 1,
}
UMBRALES = {"amarillo": 8, "naranja": 18, "rojo": 30}


def factor_confirmacion(estado: str, confirmaciones: int) -> float:
    """0 si es falso/archivado; 1.0 sin confirmaciones, hasta 1.5 con 3 o más."""
    if estado in ("falso", "archivado"):
        return 0.0
    c = min(max(confirmaciones, 0), 3)
    return 1 + (c / 3) * 0.5


def peso_reporte(r: Reporte, ahora: datetime | None = None) -> float:
    """peso = gravedad × factor_confirmacion × 0.5^(días / vida_media)"""
    ahora = ahora or datetime.now(timezone.utc)
    dias = max(0.0, (ahora - r.fecha).total_seconds() / 86400)
    return r.gravedad * factor_confirmacion(r.estado, r.confirmaciones) * 0.5 ** (
        dias / settings.vida_media_dias
    )


def temperatura(reportes: list[Reporte], ahora: datetime | None = None) -> float:
    return sum(peso_reporte(r, ahora) for r in reportes)


def nivel(t: float) -> str:
    if t > UMBRALES["rojo"]:
        return "rojo"
    if t >= UMBRALES["naranja"]:
        return "naranja"
    if t >= UMBRALES["amarillo"]:
        return "amarillo"
    return "verde"