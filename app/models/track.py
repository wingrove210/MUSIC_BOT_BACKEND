from sqlalchemy import Column, Integer, String
from database import Base

class Track(Base):
    __tablename__ = "tracks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    artist = Column(String, index=True)
    album = Column(String, index=True)
    duration = Column(Integer, index=True)
    genre = Column(String, index=True)
    release_date = Column(String, index=True)
    url = Column(String, unique=True)  # Хранит путь к файлу
