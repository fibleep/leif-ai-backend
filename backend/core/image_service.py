from uuid import UUID

from fastapi import Depends
from starlette.responses import Response

from backend.db.dao.echo_dao import EchoDAO
from backend.db.dao.explained_image_dao import ExplainedImageDAO
import io
import logging

import numpy as np
from fastapi import APIRouter, File, UploadFile
from fastapi.param_functions import Depends
from PIL import Image
from starlette.responses import Response

from backend.core.assistant.llm_engine.gpt_engine import GPTEngine
from backend.core.image_parser.filename_parser import FilenameParser
from backend.core.image_parser.gpt4_vision_parser import GPTParser
from backend.core.image_parser.image_engine import ImageEngine
from backend.core.indexer.index_engine import IndexEngine
from backend.db.dao.explained_image_dao import ExplainedImageDAO
from backend.models import explained_image
from backend.models.explained_image import ExplainedImage
from backend.models.image_extraction_format import (
    DescriptionExtractionFormat,
    DirectionExtractionFormat,
)
from backend.models.region import Region
from backend.web.api.chat.dtos.explained_image_dto import ExplainedImageDTO
from backend.web.api.images.dtos.explained_image_dto import UpdateExplainedImageDTO


class ImageService:
    async def save_image(
        self,
        echo_id: UUID,
        explained_image_dao: ExplainedImageDAO,
        echo_dao: EchoDAO,
        file: UploadFile = File(...),
        info_in_file_name: bool = False,
    ) -> Response:
        """
        Receive an image and process it.
        """

        echo = await echo_dao.get(echo_id)
        if not echo:
            return Response(status_code=404)
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        image = np.array(image)
        # Get image dimensions
        height, width, _ = image.shape
        # Define regions based on the estimated location of the texts
        # Bottom left corner

        bottom_left_region = (
        0, int(height * 0.85), int(width * 0.5), int(height * 0.2))
        # Bottom right corner
        bottom_right_region = (
            int(width * 0.9),
            int(height * 0.97),
            int(width * 0.5),
            int(height * 0.5),
        )

        # Create regions to extract
        region_description = Region(
            extraction_format=DescriptionExtractionFormat,
            region=bottom_left_region,
        )
        region_direction = Region(
            extraction_format=DirectionExtractionFormat,
            region=bottom_right_region,
        )

        # Create engines
        if info_in_file_name:
            parsing_strategy = FilenameParser(filename=file.filename)
        else:
            parsing_strategy = GPTParser()
        image_engine = ImageEngine(parsing_strategy,
                                   [region_description, region_direction])
        llm_engine = GPTEngine(model_name="gpt-4")
        index_engine = IndexEngine()

        if not info_in_file_name:
            split_images = image_engine.split_into_regions(
                image,
            )  # Retrieve the regions DIRECTION and DESCRIPTION

            description: DescriptionExtractionFormat = image_engine.parse(
                split_images[0][1],
                split_images[0][0],
            )  # Parse the image and extract the description
            direction: DirectionExtractionFormat = image_engine.parse(
                split_images[1][1],
                split_images[1][0],
            )
        else:
            description: DescriptionExtractionFormat = image_engine.parse(
                image, DescriptionExtractionFormat
            )
            direction: DirectionExtractionFormat = image_engine.parse(
                image, DirectionExtractionFormat
            )

        print(description)
        print(direction)
        ai_comment = image_engine.parse(
            image,
            None,
        )  # Generate a general comment about the image
        ai_comment_vector = llm_engine.create_embeddings(
            ai_comment,
        )  # Create a vector for the general comment
        # Create the explained image
        await explained_image_dao.create_explained_image(
            image,
            description[0].comment,
            description[0].date,
            description[0].latitude,
            description[0].longitude,
            description[0].altitude,
            description[0].location,
            direction[0].direction if direction else None,
            ai_comment,
            ai_comment_vector,
            echo
        )
