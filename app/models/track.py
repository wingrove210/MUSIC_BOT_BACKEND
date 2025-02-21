from sqlalchemy import Column, Integer, MetaData, String
from sqlalchemy.orm import DeclarativeMeta, declarative_base

Base: DeclarativeMeta = declarative_base()
metadata = MetaData()

class Track(Base):
    __tablename__ = "tracks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    artist = Column(String, index=True)
    duration = Column(String, index=True)
    url = Column(String, index=True)  # Хранит путь к файлу
    image = Column(String, index=True)  # Новое поле для изображения
