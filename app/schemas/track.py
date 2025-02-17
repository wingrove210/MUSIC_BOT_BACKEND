from pydantic import BaseModel

class TrackCreate(BaseModel):
    name: str
    artist: str
    album: str
    duration: int
    genre: str
    release_date: str

class TrackResponse(TrackCreate):
    id: int
    url: str  # Теперь отдаём ссылку на скачивание

    class Config:
        orm_mode = True
