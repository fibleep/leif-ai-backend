from enum import Enum

from pydantic.v1 import BaseModel, Field


class Direction(str, Enum):
    N = "N"
    NE = "NE"
    E = "E"
    SE = "SE"
    S = "S"
    SW = "SW"
    W = "W"
    NW = "NW"


class ImageExtractionFormat(BaseModel):
    class Config:
        arbitrary_types_allowed = True


class DescriptionExtractionFormat(ImageExtractionFormat):
    comment: str = Field(..., alias="comment on the image")
    date: str = Field(..., alias="date the image was taken")
    latitude: str = Field(..., alias="latitude of the image")
    longitude: str = Field(..., alias="longitude of the image")
    altitude: str = Field(..., alias="altitude of the image")
    location: str = Field(..., alias="location of the image")

    class Config:
        arbitrary_types_allowed = True


class DirectionExtractionFormat(ImageExtractionFormat):
    direction: Direction = Field(..., alias="direction the camera is facing")

    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True
