from base64 import b64encode
from typing import List

import cv2
import numpy as np

from backend.models.region import Region

from .image_parsing_strategy import ImageParsingStrategy


class ImageEngine:
    """
    Manipulate an image and then interpret it
    """

    def __init__(
        self,
        parsing_strategy: ImageParsingStrategy,
        default_regions: List[Region],
    ) -> None:
        self._parsing_strategy = parsing_strategy
        self.default_regions = default_regions

    def split_into_regions(self, img):
        """
        Split the image into regions.
        """
        # Load the image
        extracted_images = []
        for region in self.default_regions:
            x, y, w, h = region.region
            # Crop the image
            cropped_img = img[y : y + h, x : x + w]
            # Sharpen the cropped image
            sharpened_cropped_img = self.sharpen_image(cropped_img)
            extracted_images.append((region.extraction_format, sharpened_cropped_img))

        return extracted_images

    def sharpen_image(self, image):
        # Define the sharpening kernel
        sharpening_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        # Apply the kernel to the image
        sharpened_image = cv2.filter2D(image, -1, sharpening_kernel)
        return sharpened_image

    def encode_image_to_base64(self, image_array):
        """
        Encode image array to base64 string.
        """
        # Convert the image array to raw bytes.
        success, encoded_image = cv2.imencode(".png", image_array)

        # If conversion was successful, proceed to encode as base64.
        if success:
            # Convert to base64 encoding and return the result.
            base64_string = b64encode(encoded_image.tobytes()).decode("utf-8")
            return base64_string
        else:
            raise ValueError("Image encoding failed")

    def parse(self, image, format):
        """
        Parse the image.
        """
        # Split the image into regions.
        # Encode the image to base64.
        encoded_image = self.encode_image_to_base64(image)
        parsed_image = self._parsing_strategy.parse(encoded_image, format)
        return parsed_image
