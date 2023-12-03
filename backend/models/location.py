from pydantic import BaseModel, Field, validator


class Location(BaseModel):
    """Location model."""

    location: str = Field(..., description="Get the most recent location.")

    @validator("location")
    def check_location(cls, value):
        if value is not None and not value.isalpha():
            raise ValueError("Location must only contain letters")
        return value

    class Config:
        arbitrary_types_allowed = True
