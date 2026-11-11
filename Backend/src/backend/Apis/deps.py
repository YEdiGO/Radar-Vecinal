from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from backend.Repositories.database import get_db
from backend.Repositories.models import Usuario
from backend.Repositories.usuario_repository import UsuarioRepository
from backend.Services.security import decodificar_token

bearer = HTTPBearer(auto_error=False)
Db = Annotated[Session, Depends(get_db)]


def usuario_actual(
    creds: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)], db: Db
) -> Usuario:
    no_auth = HTTPException(status.HTTP_401_UNAUTHORIZED, "Sesión no válida o expirada.")
    if not creds:
        raise no_auth
    data = decodificar_token(creds.credentials)
    if not data:
        raise no_auth
    try:
        id_usuario = int(data["sub"])
    except (KeyError, TypeError, ValueError):
        raise no_auth
    usuario = UsuarioRepository(db).por_id(id_usuario)
    if not usuario:
        raise no_auth
    return usuario


def solo_municipalidad(usuario: Annotated[Usuario, Depends(usuario_actual)]) -> Usuario:
    if usuario.rol != "municipalidad":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Acción exclusiva de la Municipalidad.")
    return usuario


def solo_vecino(usuario: Annotated[Usuario, Depends(usuario_actual)]) -> Usuario:
    if usuario.rol != "vecino":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Acción exclusiva de los vecinos.")
    return usuario


Actual = Annotated[Usuario, Depends(usuario_actual)]
Muni = Annotated[Usuario, Depends(solo_municipalidad)]
Vecino = Annotated[Usuario, Depends(solo_vecino)]