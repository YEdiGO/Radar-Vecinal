from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from backend.config import settings


def hash_password(clave: str) -> str:
    return bcrypt.hashpw(clave.encode(), bcrypt.gensalt()).decode()


def verify_password(clave: str, hash_: str) -> bool:
    try:
        return bcrypt.checkpw(clave.encode(), hash_.encode())
    except ValueError:
        return False


def crear_token(id_usuario: int, rol: str) -> str:
    exp = datetime.now(timezone.utc) + timedelta(minutes=settings.token_minutos)
    return jwt.encode(
        {"sub": str(id_usuario), "rol": rol, "exp": exp},
        settings.secret_key,
        algorithm=settings.algorithm,
    )


def decodificar_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except jwt.PyJWTError:
        return None