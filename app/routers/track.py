import os
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.models.track import Track
from app.services.files import get_url, get_url_music

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

track_router = APIRouter()

@track_router.post("/tracks")
async def create_track(
    name: str = Form(...),
    artist: str = Form(...),
    duration: str = Form(...),
    image: UploadFile = File(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_async_session),
):
    file_path = f"{UPLOAD_DIR}/{file.filename}"
    url_image = await get_url([image])
    url_music = await get_url_music([file])
    # Save file
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Create new track object
    new_track = Track(
        name=name,
        artist=artist,
        duration=duration,
        url=url_music[0],
        image=url_image[0],
    )

    query = insert(Track).values(name=name,
                                 artist=artist,
                                 duration=duration,
                                 url=url_music[0],
                                 image=url_image[0],)
    await db.execute(query)
    await db.commit()
    return new_track

# Get all tracks
@track_router.get("/tracks")
async def get_tracks(db: AsyncSession = Depends(get_async_session)):
    query = select(Track)
    data = await db.execute(query)
    datas = data.mappings().all()
    tracks = []
    for row in datas:
        tracks.append(row["Track"])
    return tracks

@track_router.get("/tracks/{track_id}")
async def get_track(track_id: int, db: AsyncSession = Depends(get_async_session)):
    query = select(Track).where(Track.id == track_id)
    result = await db.execute(query)
    track = result.scalar_one_or_none()
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    return track

# @track_router.get("/tracks/{track_id}/download")
# async def download_track(track_id: int, db: AsyncSession = Depends(get_async_session)):
#     query = select(Track).where(Track.id == track_id)
#     result = await db.execute(query)
#     track = result.scalar_one_or_none()
#     if not track:
#         raise HTTPException(status_code=404, detail="Track not found")

#     file_path = track.url
#     if not os.path.exists(file_path):
#         raise HTTPException(status_code=404, detail="File not found")

#     return FileResponse(path=file_path, filename=os.path.basename(file_path), media_type='audio/mpeg')

@track_router.delete("/tracks/{track_id}")
async def delete_track(track_id: int, db: AsyncSession = Depends(get_async_session)):
    query = select(Track).where(Track.id == track_id)
    result = await db.execute(query)
    track = result.scalar_one_or_none()
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")

    file_path = track.url
    if os.path.exists(file_path):
        os.remove(file_path)

    stmt = delete(Track).where(Track.id == track_id)
    await db.execute(stmt)
    await db.commit()
    return track
