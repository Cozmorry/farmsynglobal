# backend/main.py
import os
import importlib
import pkgutil
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.routing import APIRoute

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from backend.core.limiter import limiter
from backend.core.database import init_db
from dotenv import load_dotenv

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()
ENV = os.getenv("ENV", "development")
FRONTEND_URLS = os.getenv("FRONTEND_URLS", "").split(",")  # comma-separated list

# -----------------------------
# Initialize Logging
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger("FarmSyn")

# -----------------------------
# Swagger Servers (Dev vs Prod)
# -----------------------------
swagger_servers = [
    {"url": "https://api.farmsynglobal.com"} if ENV == "production" else {"url": "http://127.0.0.1:8000"},
]

# -----------------------------
# Create FastAPI App
# -----------------------------
app = FastAPI(
    title="FarmSyn Global ERP",
    description="Comprehensive integrated farm management ERP.",
    version="1.0.0",
    contact={
        "name": "FarmSyn Global",
        "email": "support@farmsynglobal.com",
    },
    license_info={"name": "Proprietary License"},
    servers=swagger_servers,
)

# -----------------------------
# Rate Limiting
# -----------------------------
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# -----------------------------
# CORS Middleware
# -----------------------------
if ENV == "production":
    allowed_origins = FRONTEND_URLS or [
        "https://www.farmsynglobal.com",
        "https://farmsynglobal.com",
        "https://api.farmsynglobal.com",
    ]
else:
    allowed_origins = ["*"]  # allow all local dev origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# JWT Authentication
# -----------------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# -----------------------------
# Load Routers Dynamically
# -----------------------------
def load_all_module_routers():
    import backend.modules as modules_package
    logger.info("Discovering and loading module routers...")

    for module_info in pkgutil.iter_modules(modules_package.__path__):
        module_name = module_info.name
        router_path = f"backend.modules.{module_name}.router"

        try:
            imported_module = importlib.import_module(router_path)
            if hasattr(imported_module, "router"):
                app.include_router(imported_module.router, prefix="/api/v1")
                logger.info(f" → Loaded router for module: '{module_name}'")
        except ModuleNotFoundError:
            logger.warning(f" ! Skipping '{module_name}' (router.py not found)")
        except Exception as e:
            logger.error(f" ! Failed to load module '{module_name}': {e}")

# -----------------------------
# Fix Duplicate OpenAPI operation_id
# -----------------------------
def fix_duplicate_operation_ids(app: FastAPI):
    seen = {}
    for route in app.routes:
        if isinstance(route, APIRoute) and route.operation_id:
            if route.operation_id in seen:
                suffix = route.name or "endpoint"
                route.operation_id = f"{route.operation_id}_{suffix}"
            else:
                seen[route.operation_id] = route

# -----------------------------
# Startup / Shutdown Events
# -----------------------------
@app.on_event("startup")
def on_startup():
    logger.info("🚀 Starting FarmSyn ERP backend...")
    init_db()
    load_all_module_routers()
    fix_duplicate_operation_ids(app)
    logger.info("✅ FarmSyn backend started successfully!")

@app.on_event("shutdown")
def on_shutdown():
    logger.info("🛑 Shutting down FarmSyn backend...")

# -----------------------------
# System Endpoints
# -----------------------------
@app.get("/", tags=["System"])
def root():
    return {"message": "Welcome to FarmSyn Global ERP API!"}

@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok"}

@app.get("/hello", tags=["System"])
def hello():
    return {"message": "Hello from FarmSyn Global ERP backend!"}
