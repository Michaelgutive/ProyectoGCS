from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import tasks

# ── Crear tablas en la base de datos ────────────────────────────
Base.metadata.create_all(bind=engine)

# ── Inicializar FastAPI ─────────────────────────────────────────
app = FastAPI(
    title="Task Manager API",
    description=(
        "API REST para gestión de tareas. Proyecto CI/CD con GitHub Actions, Docker y Render."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ─────────────────────────────────────────────────────
app.include_router(tasks.router)


# ── Health Check ────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
def health_check():
    """Endpoint de health check para monitoreo y CI/CD."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "service": "task-manager-api",
    }
