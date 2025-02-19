import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from models.track import Track
from schemas.track import TrackCreate, TrackResponse
from fastapi.responses import JSONResponse, FileResponse
from fastapi import Form
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Создаём папку, если её нет

track_router = APIRouter()

# 🔹 Загрузка нового трека с файлом

@track_router.post("/tracks", response_model=TrackResponse)
async def create_track(
    name: str = Form(...),
    artist: str = Form(...),
    duration: int = Form(...),
    image: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    file_path = f"{UPLOAD_DIR}/{file.filename}"

    # Сохраняем файл
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Создаём новый объект трека
    new_track = Track(
        name=name,
        artist=artist,
        duration=duration,
        url=file_path,
        image=image,
    )
    
    db.add(new_track)
    db.commit()
    db.refresh(new_track)
    return new_track


# 🔹 Получение всех треков
@track_router.get("/tracks", response_model=list[TrackResponse])
async def get_tracks(db: Session = Depends(get_db)):
    return db.query(Track).all()

# 🔹 Получение одного трека по ID
@track_router.get("/tracks/{track_id}", response_model=TrackResponse)
async def get_track(track_id: int, db: Session = Depends(get_db)):
    track = db.query(Track).filter(Track.id == track_id).first()
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    return track

# 🔹 Раздача файлов (URL)
@track_router.get("/tracks/{track_id}/download")
async def download_track(track_id: int, db: Session = Depends(get_db)):
    track = db.query(Track).filter(Track.id == track_id).first()
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")

    file_path = track.url
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(path=file_path, filename=os.path.basename(file_path), media_type='audio/mpeg')

# 🔹 Удаление трека по ID
@track_router.delete("/tracks/{track_id}", response_model=TrackResponse)
async def delete_track(track_id: int, db: Session = Depends(get_db)):
    track = db.query(Track).filter(Track.id == track_id).first()
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")

    # Удаляем файл с диска
    file_path = track.url
    if os.path.exists(file_path):
        os.remove(file_path)

    # Удаляем трек из базы данных
    db.delete(track)
    db.commit()
    return track
