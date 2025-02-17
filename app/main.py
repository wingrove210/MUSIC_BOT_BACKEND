from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import Base, engine
from routers.track import track_router

app = FastAPI()

# Настройка CORS
origins = [
    "http://localhost:5173",  # разрешаем доступ с локального хоста
    "http://localhost:3000",  # если фронтенд работает на порту 3000 (например, React)
    "https://your-frontend-url.com",  # добавьте URL вашего фронтенда
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Список источников, которым разрешено делать запросы
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы (GET, POST и т.д.)
    allow_headers=["*"],  # Разрешаем все заголовки
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
async def home():
    return {"message": "Hello, FastAPI!"}

app.include_router(track_router)

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
