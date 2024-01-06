from pydantic import BaseModel


class ExplainedImageDTO(BaseModel):
    """ExplainedImage model"""

    title: str
    date: str
    image: str
    latitude: float
    longitude: float
    altitude: int
    location: str
    direction: str | None
    additional_comment: str
