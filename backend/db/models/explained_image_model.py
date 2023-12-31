from pgvector.sqlalchemy import Vector
from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import mapped_column

from backend.db.base import Base


class ExplainedImageModel(Base):
    __tablename__ = "explained_images"
    id = mapped_column(Integer(), primary_key=True)
    image = mapped_column(String(), nullable=False)
    title = mapped_column(String())
    date = mapped_column(String())
    latitude = mapped_column(Float())
    longitude = mapped_column(Float())
    altitude = mapped_column(Integer())
    location = mapped_column(String())
    direction = mapped_column(String())
    additional_comment = mapped_column(String())
    additional_comment_vector = mapped_column(Vector(), nullable=False)
