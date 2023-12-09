from backend.models.image_extraction_format import (
    DescriptionExtractionFormat,
    DirectionExtractionFormat,
)

from .image_parsing_strategy import ImageParsingStrategy


class FilenameParser(ImageParsingStrategy):
    def __init__(self, filename):
        self.filename = filename

    def parse(self, image, format):
        """
        Parse the image using vision and extract it into a format

        :param image: image to parse, base64
        """
        if format.__class__.__name__ == "DescriptionExtractionFormat":
            return self.parse_description()
        elif format.__class__.__name__ == "DirectionExtractionFormat":
            return self.parse_direction()
        return

    def parse_description(self):
        """
        Parse the description from the filename
        """
        lines = self.filename.split("_")

        comment = lines[0]
        date = lines[1]

        description = DescriptionExtractionFormat()
        return description

    def parse_direction(self):
        """
        Parse the direction from the filename
        """
        direction = DirectionExtractionFormat()
        return direction
