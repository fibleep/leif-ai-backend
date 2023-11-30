from typing import Tuple, Type

from pydantic import BaseModel

from .image_extraction_format import ImageExtractionFormat


class Region(BaseModel):
    """Region model"""

    extraction_format: Type[ImageExtractionFormat]
    region: Tuple[int, int, int, int]
