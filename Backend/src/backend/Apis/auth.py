from fastapi import APIRouter, status

from backend.Apis.deps import Actual, Db
from backend.Schemas.auth import LoginIn, RegistroIn, TokenOut, UsuarioOut
from backend.Services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/registro", response_model=TokenOut, status_code=status.HTTP_201_CREATED)
def registro(datos: RegistroIn, db: Db):
    return AuthService(db).registrar(datos)


@router.post("/login", response_model=TokenOut)
def login(datos: LoginIn, db: Db):
    return AuthService(db).login(datos)


@router.get("/me", response_model=UsuarioOut)
def me(usuario: Actual):
    return usuario