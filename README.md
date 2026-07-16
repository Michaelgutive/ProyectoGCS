# 🚀 Task Manager API — CI/CD Pipeline

![CI Pipeline](https://github.com/Michaelgutive/proyectogcs/actions/workflows/ci.yml/badge.svg)
![CD Staging](https://github.com/Michaelgutive/proyectogcs/actions/workflows/cd-staging.yml/badge.svg)
![CD Production](https://github.com/Michaelgutive/proyectogcs/actions/workflows/cd-production.yml/badge.svg)

API REST para gestión de tareas construida con **FastAPI**, con un pipeline **CI/CD profesional** usando **GitHub Actions**, **Docker**, y **Render**.

---

## 📋 Tabla de Contenidos

- [Arquitectura CI/CD](#-arquitectura-cicd)
- [Tecnologías](#-tecnologías)
- [API Endpoints](#-api-endpoints)
- [Pipeline CI/CD](#-pipeline-cicd)
- [Configuración Local](#-configuración-local)
- [Configuración de GitHub](#-configuración-de-github)
- [Equipo](#-equipo)

---

## 🏗️ Arquitectura CI/CD

```
┌─────────────┐     ┌──────────────────────────────────────────────────────────┐
│  Developer   │────▶│                   GitHub Actions                         │
│  Push / PR   │     │  ┌──────┐  ┌───────┐  ┌──────────┐  ┌──────────────┐   │
└─────────────┘     │  │ Lint │─▶│ Tests │─▶│ Security │─▶│ Docker Build │   │
                    │  └──────┘  └───────┘  └──────────┘  └──────┬───────┘   │
                    └─────────────────────────────────────────────┼───────────┘
                                                                  │
                                                                  ▼
                    ┌─────────────────┐          ┌─────────────────────────┐
                    │  Docker Image   │─────────▶│     Render (Cloud)      │
                    │  (GHCR)         │          │  ┌─────────┐ ┌───────┐  │
                    └─────────────────┘          │  │ Staging │ │  Prod │  │
                                                 │  └─────────┘ └───────┘  │
                    ┌─────────────────┐          └─────────────────────────┘
                    │    Discord      │◀─── Notificaciones automáticas
                    └─────────────────┘
```

---

## 🛠️ Tecnologías

| Categoría | Tecnología |
|---|---|
| **Backend** | Python 3.11, FastAPI |
| **Base de Datos** | SQLite (SQLAlchemy ORM) |
| **Testing** | Pytest, Coverage |
| **Linting** | Ruff |
| **Seguridad** | Bandit (SAST), pip-audit |
| **Container** | Docker, Docker Compose |
| **Registry** | GitHub Container Registry (GHCR) |
| **CI/CD** | GitHub Actions |
| **Deploy** | Render (Cloud PaaS) |
| **Notificaciones** | Discord Webhooks |

---

## 📡 API Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/health` | Health check del servicio |
| `GET` | `/tasks` | Listar todas las tareas |
| `GET` | `/tasks/{id}` | Obtener tarea por ID |
| `POST` | `/tasks` | Crear nueva tarea |
| `PUT` | `/tasks/{id}` | Actualizar tarea |
| `DELETE` | `/tasks/{id}` | Eliminar tarea |
| `GET` | `/docs` | Documentación interactiva (Swagger) |
| `GET` | `/redoc` | Documentación alternativa (ReDoc) |

---

## 🔄 Pipeline CI/CD

### CI Pipeline (`ci.yml`)
Se ejecuta en cada **push** y **pull request** a `main` y `develop`:

| Etapa | Herramienta | Descripción |
|---|---|---|
| 🔍 **Lint** | Ruff | Verifica estilo de código y formato |
| 🧪 **Tests** | Pytest | Corre tests en Python 3.10, 3.11, 3.12 (matrix) con 80% cobertura mínima |
| 🛡️ **Security** | Bandit + pip-audit | Escaneo de seguridad en código y dependencias |
| 🐳 **Docker** | Docker + GHCR | Build y push de imagen al registry |
| 🔔 **Notify** | Discord | Notificación de resultado |

### CD Staging (`cd-staging.yml`)
Se ejecuta automáticamente cuando CI pasa en `develop`:
- Deploy automático a staging vía Render deploy hook
- Health check post-deploy
- Notificación a Discord

### CD Production (`cd-production.yml`)
Se ejecuta cuando CI pasa en `main`:
- ⚠️ **Requiere aprobación manual** (Environment Protection)
- Deploy a producción vía Render deploy hook
- Creación automática de GitHub Release con versionado semántico
- Notificación a Discord

---

## 💻 Configuración Local

### Prerequisitos
- Python 3.10+
- Docker (opcional)

### Sin Docker
```bash
# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Ejecutar la API
uvicorn app.main:app --reload

# Ejecutar tests
pytest --cov=app --cov-report=term-missing

# Ejecutar linter
ruff check .
ruff format --check .
```

### Con Docker
```bash
docker compose up --build
```

La API estará disponible en `http://localhost:8000` y la documentación en `http://localhost:8000/docs`.

---

## ⚙️ Configuración de GitHub

### Secrets requeridos
Configurar en **Settings → Secrets and variables → Actions**:

| Secret | Descripción |
|---|---|
| `DISCORD_WEBHOOK_URL` | Webhook URL de tu canal de Discord |
| `RENDER_DEPLOY_HOOK_STAGING` | Deploy Hook URL del servicio staging en Render |
| `RENDER_DEPLOY_HOOK_PRODUCTION` | Deploy Hook URL del servicio producción en Render |
| `STAGING_URL` | URL base de la app en staging (ej: `https://proyectogcs-staging.onrender.com`) |
| `PRODUCTION_URL` | URL base de la app en producción (ej: `https://proyectogcs-production.onrender.com`) |

### Environments
Configurar en **Settings → Environments**:

1. **staging** — Sin protección adicional (deploy automático)
2. **production** — Con **Required reviewers** (al menos 2 miembros del equipo)

### Branch Protection
Configurar en **Settings → Branches → Branch protection rules**:

- **`main`**: Require PR, 2 approvals, require status checks (CI Pipeline)
- **`develop`**: Require PR, 1 approval, require status checks (CI Pipeline)

---

## 👥 Equipo

| Miembro | Rol |
|---|---|
| Miembro 1 | Backend Developer |
| Miembro 2 | Backend Developer |
| Miembro 3 | DevOps — CI Pipeline |
| Miembro 4 | DevOps — CI Pipeline |
| Miembro 5 | DevOps — CD Pipeline |
| Miembro 6 | DevOps — CD Pipeline |

---

## 📄 Licencia

Proyecto académico — Gestión de Configuración de Software.
