from pydantic import BaseModel

class VideoCreate(BaseModel):
    url: str

class VideoResponse(VideoCreate):
    id: int

    class Config:
        orm_mode = True
