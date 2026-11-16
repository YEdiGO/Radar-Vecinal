import random
from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.Repositories.models import Barrio, Reporte, Usuario, ahora
from backend.Services.security import hash_password
from backend.Services.temperatura import GRAVEDAD

# Polígonos ilustrativos [lat, lng]; NO son límites oficiales.
BARRIOS = [
    ("b1", "San Carlos", [[-12.061, -75.204], [-12.057, -75.203], [-12.056, -75.196], [-12.062, -75.196], [-12.064, -75.200]]),
    ("b2", "Azapampa", [[-12.069, -75.209], [-12.069, -75.202], [-12.073, -75.199], [-12.077, -75.203], [-12.076, -75.210]]),
    ("b3", "Ocopilla", [[-12.065, -75.201], [-12.062, -75.195], [-12.065, -75.190], [-12.071, -75.192], [-12.072, -75.197]]),
    ("b4", "Pío Pata", [[-12.058, -75.214], [-12.053, -75.212], [-12.053, -75.206], [-12.057, -75.204], [-12.061, -75.209]]),
    ("b5", "Cerrito de la Libertad", [[-12.063, -75.208], [-12.061, -75.204], [-12.064, -75.200], [-12.067, -75.201], [-12.069, -75.205], [-12.067, -75.209]]),
]
CANTIDAD = {"b1": 2, "b2": 14, "b3": 8, "b4": 5, "b5": 3}
TIPOS = list(GRAVEDAD)
TEXTOS = {
    "asalto_robo": "Arrebato de celular a un transeúnte.",
    "pandillaje": "Grupo de jóvenes agrediendo a transeúntes.",
    "alcohol_drogas": "Consumo de alcohol en la vía pública.",
    "falta_alumbrado": "Poste sin luz, la calle queda a oscuras.",
    "actividad_sospechosa": "Persona merodeando viviendas.",
    "otro": "Incidente reportado por vecinos.",
}


def _punto(rng: random.Random, poligono: list[list[float]]) -> tuple[float, float]:
    cx = sum(p[0] for p in poligono) / len(poligono)
    cy = sum(p[1] for p in poligono) / len(poligono)
    v = rng.choice(poligono)
    t = rng.uniform(0, 0.6)
    return cx + t * (v[0] - cx), cy + t * (v[1] - cy)


def sembrar(db: Session) -> None:
    if db.scalar(select(Barrio.id).limit(1)):
        return
    for id_, nombre, poligono in BARRIOS:
        db.add(Barrio(id=id_, nombre=nombre, poligono=poligono))
    db.flush()

    muni = db.scalar(select(Usuario).where(Usuario.correo == "muni@huancayo.gob.pe"))
    if not muni:
        muni = Usuario(
            nombre="Gerencia de Seguridad Ciudadana", correo="muni@huancayo.gob.pe",
            password_hash=hash_password("123456"), rol="municipalidad",
            institucion="Municipalidad Provincial de Huancayo",
        )
        db.add(muni)
    vecino = db.scalar(select(Usuario).where(Usuario.correo == "vecino@barrio.com"))
    if not vecino:
        vecino = Usuario(
            nombre="Rosa Quispe", correo="vecino@barrio.com",
            password_hash=hash_password("123456"), rol="vecino", id_barrio="b1",
        )
        db.add(vecino)
    db.flush()

    rng = random.Random(42)
    for id_, _, poligono in BARRIOS:
        for _ in range(CANTIDAD[id_]):
            tipo = rng.choices(TIPOS, weights=[4, 2, 3, 3, 2, 1])[0]
            lat, lng = _punto(rng, poligono)
            db.add(Reporte(
                id_usuario=vecino.id, id_barrio=id_, lat=lat, lng=lng, tipo=tipo,
                gravedad=GRAVEDAD[tipo], descripcion=TEXTOS[tipo],
                fecha=ahora() - timedelta(days=rng.uniform(0, 20), hours=rng.uniform(0, 12)),
            ))
    db.commit()