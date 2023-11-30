from abc import ABC, abstractmethod
from backend.models.image_extraction_format import ImageExtractionFormat


class ImageParsingStrategy(ABC):
    @abstractmethod
    def parse(self, image, format: ImageExtractionFormat):
        pass
