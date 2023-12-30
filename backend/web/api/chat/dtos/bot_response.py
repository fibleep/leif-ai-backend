from typing import List

from backend.web.api.chat.dtos.explained_image_dto import ExplainedImageDTO


class BotResponse:
    """
    Bot response model
    """
    comment: str
    destinations: List[ExplainedImageDTO]

    def __init__(self, comment: str, destinations: List[ExplainedImageDTO]):
        self.comment = comment
        self.destinations = destinations
