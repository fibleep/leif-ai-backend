from typing import List

from pydantic import BaseModel


class ImageDecision(BaseModel):
    index: List[int]

    class Config:
        arbitrary_types_allowed = True
