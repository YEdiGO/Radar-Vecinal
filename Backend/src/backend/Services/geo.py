from backend.Repositories.models import Barrio


def punto_en_poligono(lat: float, lng: float, poligono: list[list[float]]) -> bool:
    """Ray casting sobre polígonos [lat, lng]."""
    if len(poligono) < 3:
        return False
    dentro = False
    j = len(poligono) - 1
    for i in range(len(poligono)):
        y1, x1 = poligono[i]
        y2, x2 = poligono[j]
        if (y1 > lat) != (y2 > lat) and lng < (x2 - x1) * (lat - y1) / (y2 - y1) + x1:
            dentro = not dentro
        j = i
    return dentro


def barrio_del_punto(lat: float, lng: float, barrios: list[Barrio]) -> Barrio | None:
    return next((b for b in barrios if punto_en_poligono(lat, lng, b.poligono)), None)