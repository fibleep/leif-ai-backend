from typing import List

from pydantic import BaseModel

from backend.db.models.explained_image_model import ExplainedImageModel


class UpdateExplainedImageDTO(BaseModel):
    """ExplainedImage model"""
    id: int
    image: str
    title: str
    date: str
    latitude: float
    longitude: float
    altitude: int
    location: str
    direction: str
    additional_comment: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Config:
        arbitrary_types_allowed = True
