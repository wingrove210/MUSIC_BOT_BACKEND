from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.video import Video
from schemas.video import VideoCreate, VideoResponse

video_router = APIRouter()

@video_router.post("/videos", response_model=VideoResponse)
async def create_video(video: VideoCreate, db: Session = Depends(get_db)):
    new_video = Video(url=video.url)
    db.add(new_video)
    db.commit()
    db.refresh(new_video)
    return new_video

@video_router.get("/videos/{video_id}", response_model=VideoResponse)
async def get_video(video_id: int, db: Session = Depends(get_db)):
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video
