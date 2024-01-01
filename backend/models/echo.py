from uuid import UUID

from pydantic import BaseModel

from backend.models.explained_image import ExplainedImage


class Echo(BaseModel):
    id: UUID
    name: str
    explained_images: list[ExplainedImage]

    class Config:
        orm_mode = True
