from fastapi import APIRouter

from backend.Apis import acciones, alertas, auth, barrio, iniciativas, municipalidad, reportes, zonas

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(barrio.router)
api_router.include_router(zonas.router)
api_router.include_router(reportes.router)
api_router.include_router(iniciativas.router)
api_router.include_router(acciones.router)
api_router.include_router(municipalidad.router)
api_router.include_router(alertas.router)