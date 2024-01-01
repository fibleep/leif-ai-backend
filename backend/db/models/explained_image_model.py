from sqlalchemy.dialects.postgresql import UUID

from pgvector.sqlalchemy import Vector
from sqlalchemy import Integer, String, Float, ForeignKey, Column
from sqlalchemy.orm import mapped_column, relationship, Mapped

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
    direction = mapped_column(String(), nullable=True)
    additional_comment = mapped_column(String())
    additional_comment_vector = mapped_column(Vector(), nullable=False)
    echo_id:Mapped[UUID] = mapped_column(ForeignKey("echo.id"))
    echo:Mapped["EchoModel"] = relationship(back_populates="explained_images")
