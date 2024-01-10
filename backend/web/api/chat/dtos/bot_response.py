from typing import List, AsyncIterable

from backend.web.api.chat.dtos.explained_image_dto import ExplainedImageDTO


class BotResponse:
    """
    Bot response model
    """
    comment: AsyncIterable[str]
    destinations: List[ExplainedImageDTO] = []

    def __init__(self, comment: AsyncIterable[str], destinations: List[
        ExplainedImageDTO]):
        self.comment = comment
        self.destinations = destinations
