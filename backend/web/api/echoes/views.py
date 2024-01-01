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
from backend.db.dao.echo_dao import EchoDAO
from backend.db.dao.explained_image_dao import ExplainedImageDAO
from backend.models import explained_image
from backend.models.explained_image import ExplainedImage
from backend.models.image_extraction_format import (
    DescriptionExtractionFormat,
    DirectionExtractionFormat,
)
from backend.models.region import Region
from backend.web.api.chat.dtos.explained_image_dto import ExplainedImageDTO
from backend.web.api.echoes.dtos.echo_dto import EchoDTO
from backend.web.api.images.dtos.explained_image_dto import UpdateExplainedImageDTO

router = APIRouter()


@router.post("/")
async def create_echo(
    created_echo: EchoDTO,
    echo_dao: EchoDAO = Depends(),
):
    """
    Create a new echo
    """
    echo = await echo_dao.create(created_echo)
    return echo


@router.get("/")
async def get_all_echoes(
    echo_dao: EchoDAO = Depends(),
):
    """
    Get all echoes
    """
    echoes = await echo_dao.get_all()
    return echoes
