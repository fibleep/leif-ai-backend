from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, Integer, String
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import mapped_column

from backend.settings import settings
from sqlalchemy.orm import Mapped, mapped_column
from backend.db.base import Base


class ExplainedImageModel(Base):
    __tablename__ = "explained_images"
    id = mapped_column(Integer(), primary_key=True)
    image = mapped_column(String(), nullable=False)
    comment = mapped_column(String())
    date = mapped_column(String())
    latitude = mapped_column(String())
    longitude = mapped_column(String())
    altitude = mapped_column(String())
    location = mapped_column(String())
    direction = mapped_column(String())
    ai_comment = mapped_column(String())
    ai_comment_vector = mapped_column(Vector(), nullable=False)
