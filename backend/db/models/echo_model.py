import uuid
from typing import List

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, Mapped

from backend.db.base import Base
from backend.db.models.explained_image_model import ExplainedImageModel


class EchoModel(Base):
    __tablename__ = 'echo'

    id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    name = Column(String)

    explained_images: Mapped[List["ExplainedImageModel"]] = relationship(lazy='select')
