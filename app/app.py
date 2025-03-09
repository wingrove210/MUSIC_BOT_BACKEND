from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routers.main import router
from app.core.logger import logger
from app.core.config import settings

app = FastAPI(
    title="Music Bot API",
    description="API для музыкального бота",
    version="1.0.0",
    docs_url="/api/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url="/api/redoc" if settings.ENVIRONMENT == "development" else None
)

# Настройка разрешенных источников
origins = [
    "*"
]

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up Music Bot API")
    logger.info(f"Environment: {settings.ENVIRONMENT}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Music Bot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"]
)
# Монтируем статические файлы с настройками кэширования
app.mount(
    "/uploads",
    StaticFiles(
        directory="uploads",
        html=True,
        check_dir=True,
        follow_symlink=True
    ),
    name="uploads"
)

app.include_router(router, prefix="/api")