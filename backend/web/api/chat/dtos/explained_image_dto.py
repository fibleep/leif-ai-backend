from pydantic import BaseModel


class ExplainedImageDTO(BaseModel):
    """ExplainedImage model"""

    comment: str
    date: str
    latitude: str
    longitude: str
    altitude: str
    location: str
    direction: str
    ai_comment: str
