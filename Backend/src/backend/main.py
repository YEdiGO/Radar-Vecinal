from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.Apis import api_router
from backend.config import settings
from backend.Repositories import models  # noqa: F401  (registra las tablas)
from backend.Repositories.database import Base, SessionLocal, engine
from backend.Services.seed_service import sembrar


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        sembrar(db)
    yield


app = FastAPI(title="Radar Vecinal API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.get("/", tags=["Salud"])
def raiz():
    return {"app": "Radar Vecinal", "estado": "ok"}