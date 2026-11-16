from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from backend.Repositories.barrio_repository import BarrioRepository
from backend.Repositories.usuario_repository import UsuarioRepository
from backend.Schemas.auth import LoginIn, RegistroIn, TokenOut, UsuarioOut
from backend.Services.security import crear_token, hash_password, verify_password


class AuthService:
    def __init__(self, db: Session):
        self.usuarios = UsuarioRepository(db)
        self.barrios = BarrioRepository(db)

    def _token(self, usuario) -> TokenOut:
        return TokenOut(
            access_token=crear_token(usuario.id, usuario.rol),
            usuario=UsuarioOut.model_validate(usuario),
        )

    def registrar(self, datos: RegistroIn) -> TokenOut:
        if self.usuarios.por_correo(datos.correo):
            raise HTTPException(status.HTTP_409_CONFLICT, "Ese correo ya está registrado.")
        if not self.barrios.por_id(datos.id_barrio):
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Barrio no válido.")
        usuario = self.usuarios.crear(
            nombre=datos.nombre.strip(),
            correo=datos.correo.lower(),
            password_hash=hash_password(datos.clave),
            rol="vecino",  # la Municipalidad solo se crea por seed
            id_barrio=datos.id_barrio,
        )
        return self._token(usuario)

    def login(self, datos: LoginIn) -> TokenOut:
        usuario = self.usuarios.por_correo(datos.correo)
        if not usuario or not verify_password(datos.clave, usuario.password_hash):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Correo o contraseña incorrectos.")
        return self._token(usuario)