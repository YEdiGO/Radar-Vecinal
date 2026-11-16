# AGENTS.md

Radar Vecinal: Angular 22 (SSR) frontend + FastAPI/SQLAlchemy backend. Domain code, UI text, and API errors are in Spanish.

## Layout and wiring

- `Frontend/` standalone Angular app (no NgModules). `Backend/` is a `uv` project with the package under `Backend/src/backend/`.
- Backend layers: `Apis/` (routers) -> `Services/` (business rules) -> `Repositories/` (SQLAlchemy); Pydantic schemas in `Schemas/`, ORM models in `Repositories/models.py`.
- All API routers are mounted under `/api` in `Backend/src/backend/Apis/__init__.py`; FastAPI docs at `http://localhost:8000/docs`.
- Frontend calls the API through the hard-coded `http://localhost:8000/api` in `Frontend/src/app/Services/api.config.ts`.
- Auth is JWT in localStorage (`rv_token`, `rv_usuario`). Roles are `vecino` and `municipalidad`; guards live in `Services/auth.guard.ts`, backend role dependencies in `Apis/deps.py` (`Actual`, `Vecino`, `Muni`).
- Heat-map math lives only in `Backend/src/backend/Services/temperatura.py` (severity × confirmation factor × exponential time decay; thresholds 8/18/30). Serve `temperatura`/`nivel` from the API instead of reimplementing it in the UI.
- Seed polygons in `Services/seed_service.py` are illustrative but define valid report coordinates: reports whose point falls outside every polygon are rejected.

## Running

Backend (from `Backend/`): `uv sync`, then `uv run uvicorn backend.main:app --reload --port 8000`.
- Requires PostgreSQL database `radar_vecinal` to already exist (default URL in `Backend/.env`); tables are created with `Base.metadata.create_all()` on startup.
- Seeding runs only when the `barrios` table is empty. Seed logins: `muni@huancayo.gob.pe` / `123456` (municipalidad) and `vecino@barrio.com` / `123456` (vecino).
- No Alembic/migrations: model changes need a fresh/recreated database or manual SQL.

Frontend (from `Frontend/`): `npm install`, `npm start` (port 4200), `npm test` (Vitest via Angular's unit-test builder), `npm run build`.
- Single suite: `npm test -- --watch=false --filter=App` (or `--include=src/app/app.spec.ts`).
- SSR is all client-rendered (`app.routes.server.ts`), so browser APIs such as localStorage are safe in components. `npm run serve:ssr:Frontend` serves the built app on port 4000.
- Prettier is the only formatter configured (`.prettierrc`: 100 cols, single quotes, Angular HTML parser); there is no ESLint or CI.

## Conventions and gotchas

- `Services/auth.interceptor.ts` (not `auth.service.ts`) exports both the functional JWT `authInterceptor` and `mensajeError(error)`. Components import `mensajeError` from there; the interceptor reads `rv_token` directly from localStorage to avoid a DI cycle with `HttpClient`/`AuthService`.
- Declare runtime deps instead of relying on the venv: frontend assets (`bootstrap`, `bootstrap-icons`, `leaflet`, `@types/leaflet`) must stay in `Frontend/package.json` because `angular.json` references their CSS.
- Keep `uvicorn` plain, not `uvicorn[standard]`: the `[standard]` extra pulls `pyyaml`, which fails to build on this Python 3.15/Windows setup without MSVC C++ Build Tools.
- `Backend/.env` is git-ignored. `config.py` resolves it relative to the package (`Backend/.env`), so it loads regardless of the working directory.

## Verification (last run in this snapshot)

- `cd Frontend && npx tsc -p tsconfig.app.json --noEmit` -> clean.
- `cd Frontend && npm run build` -> succeeds (warnings: initial bundle 725 kB vs 500 kB budget; Leaflet not ESM).
- `cd Frontend && npm test -- --watch=false` -> 1 test passed.
- `cd Backend && uv lock --check` and `uv run python -c "import backend.main"` -> clean; OpenAPI publishes all `/api/*` routes.
- Full backend startup was **not** verified: no local PostgreSQL service was detected, and `base.metadata.create_all()` + seeding run in the lifespan hook. Create the `radar_vecinal` database and start PostgreSQL before smoke-testing login/report flows.
