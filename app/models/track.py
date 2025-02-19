from sqlalchemy import Column, Integer, String
from database import Base

class Track(Base):
    __tablename__ = "tracks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    artist = Column(String, index=True)
    duration = Column(String, index=True)
    url = Column(String, unique=True)  # Хранит путь к файлу
    image = Column(String, index=True)  # Новое поле для изображения
