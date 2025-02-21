from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.models.video import Video
from app.schemas.video import VideoCreate
from sqlalchemy import insert, select


video_router = APIRouter()

@video_router.post("/videos")
async def create_video(video: VideoCreate, db: AsyncSession = Depends(get_async_session)):
    new_video = insert(Video).values(url=video.url)
    await db.execute(new_video)
    await db.commit()
    return video

@video_router.get("/videos/{video_id}")
async def get_video(video_id: int, db: AsyncSession = Depends(get_async_session)):
    video = select(Video).where(Video.id == video_id)
    video = await db.execute(video)
    video = video.scalars().first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video
