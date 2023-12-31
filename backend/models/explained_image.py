from typing import List

from pydantic import BaseModel

from backend.db.models.explained_image_model import ExplainedImageModel


class ExplainedImage(BaseModel):
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

    def __init__(self, image):
        super().__init__(
            id=image.id,
            image=image.image,
            title=image.title,
            date=image.date,
            latitude=image.latitude,
            longitude=image.longitude,
            altitude=image.altitude,
            location=image.location,
            direction=image.direction,
            additional_comment=image.additional_comment,
        )


    class Config:
        arbitrary_types_allowed = True
