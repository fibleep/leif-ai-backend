from pydantic import BaseModel


class ExplainedImageDTO(BaseModel):
    """ExplainedImage model"""

    title: str
    date: str
    latitude: float
    longitude: float
    altitude: int
    location: str
    direction: str
    additional_comment: str
