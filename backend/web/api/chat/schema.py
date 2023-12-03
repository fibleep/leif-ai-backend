from typing import List

from pydantic import BaseModel


class Coordinates(BaseModel):
    """Coordinates model."""

    lat: float
    lng: float
    alt: float


class Geolocation(BaseModel):
    """Geolocation model."""

    loaded: bool
    coordinates: Coordinates


class Message(BaseModel):
    """Simple message model."""

    role: str
    content: str
    geolocation: Geolocation = None


class Conversation(BaseModel):
    """Simple message model."""

    messages: List[Message]
