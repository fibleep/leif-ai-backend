from pydantic import BaseModel
from .image_extraction_format import ImageExtractionFormat, DescriptionExtractionFormat, DirectionExtractionFormat
from typing import List


class ExplainedImage(BaseModel):
    """ExplainedImage model"""
    image: str
    comment: str
    date: str
    latitude: str
    longitude: str
    altitude: str
    location: str
    direction: str
    ai_comment: str
    ai_comment_vector: List[float]

    class Config:
        arbitrary_types_allowed = True

