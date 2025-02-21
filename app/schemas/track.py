from pydantic import BaseModel

class TrackCreate(BaseModel):
    name: str
    artist: str
    duration: str
    image: str
    file: str

class TrackResponse(TrackCreate):
    id: int
    url: str  # Теперь отдаём ссылку на скачивание

    class Config:
        orm_mode = True
