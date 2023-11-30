from fastapi import APIRouter

from backend.core.assistant.llm_engine.gpt_engine import GPTEngine
from backend.core.image_parser.gpt4_vision_parser import GPTParser
from backend.core.image_parser.image_engine import ImageEngine
from backend.core.indexer.index_engine import IndexEngine
from backend.models.explained_image import ExplainedImage
from backend.models.image_extraction_format import (
    DescriptionExtractionFormat,
    DirectionExtractionFormat,
)
from fastapi import File, UploadFile
import shutil
from backend.models.region import Region
import io
import numpy as np
from PIL import Image
import logging
from fastapi.param_functions import Depends
from backend.db.dao.explained_image_dao import ExplainedImageDAO

router = APIRouter()


@router.post("/", response_model=ExplainedImage)
async def submit_image(
    file: UploadFile = File(...),
    explained_image_dao: ExplainedImageDAO = Depends(),
) -> ExplainedImage:
    """
    Receive an image and process it.
    """
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    image = np.array(image)
    # Get image dimensions
    height, width, _ = image.shape
    # Define regions based on the estimated location of the texts
    # Bottom left corner

    bottom_left_region = (0, int(height * 0.85), int(width * 0.5), int(height * 0.2))
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
        extraction_format=DirectionExtractionFormat, region=bottom_right_region
    )

    # Create engines
    parsing_strategy = GPTParser()
    image_engine = ImageEngine(parsing_strategy, [region_description, region_direction])
    llm_engine = GPTEngine(model_name="gpt-4")
    index_engine = IndexEngine()

    split_images = image_engine.split_into_regions(
        image
    )  # Retrieve the regions DIRECTION and DESCRIPTION

    description: DescriptionExtractionFormat = image_engine.parse(
        split_images[0][1], split_images[0][0]
    )  # Parse the image and extract the description
    direction: DirectionExtractionFormat = image_engine.parse(
        split_images[1][1], split_images[1][0]
    )
    ai_comment = image_engine.parse(
        image, None
    )  # Generate a general comment about the image
    ai_comment_vector = llm_engine.create_embeddings(
        ai_comment
    )  # Create a vector for the general comment
    # Create the explained image
    encoded_image = image_engine.encode_image_to_base64(image)

    explained_image = ExplainedImage(
        image=encoded_image,
        comment=description[0].comment,
        date=description[0].date,
        latitude=description[0].latitude,
        longitude=description[0].longitude,
        altitude=description[0].altitude,
        location=description[0].location,
        direction=direction[0].direction,
        ai_comment=ai_comment,
        ai_comment_vector=ai_comment_vector,
    )

    await explained_image_dao.create_explained_image(explained_image)

    return explained_image
