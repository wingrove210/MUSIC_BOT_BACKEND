from pydantic import BaseModel

class TrackCreate(BaseModel):
    name: str
    artist: str
    duration: int
    image: str  # Новое поле для изображения

class TrackResponse(TrackCreate):
    id: int
    url: str  # Теперь отдаём ссылку на скачивание

    class Config:
        orm_mode = True
