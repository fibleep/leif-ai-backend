from typing import List

from pydantic import BaseModel

from backend.db.models.explained_image_model import ExplainedImageModel


class ExplainedImage(BaseModel):
    """ExplainedImage model"""
    id: int
    image: str
    comment: str
    date: str
    latitude: str
    longitude: str
    altitude: str
    location: str
    direction: str
    additional_comment: str

    def __init__(self, image):
        super().__init__(
            id=image.id,
            image=image.image,
            comment=image.comment,
            date=image.date,
            latitude=image.latitude,
            longitude=image.longitude,
            altitude=image.altitude,
            location=image.location,
            direction=image.direction,
            additional_comment=image.ai_comment,
        )
    class Config:
        arbitrary_types_allowed = True
