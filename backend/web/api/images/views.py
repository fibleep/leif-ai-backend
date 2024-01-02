import io
import logging
from uuid import UUID

import numpy as np
from fastapi import APIRouter, File, UploadFile
from fastapi.param_functions import Depends
from PIL import Image
from starlette.responses import Response

from backend.core.image_service import ImageService
from backend.core.indexer.index_engine import IndexEngine
from backend.db.dao.echo_dao import EchoDAO
from backend.db.dao.explained_image_dao import ExplainedImageDAO
from backend.models import explained_image
from backend.models.explained_image import ExplainedImage
from backend.web.api.images.dtos.explained_image_dto import UpdateExplainedImageDTO

router = APIRouter()


@router.post("/{echo_id}", response_model=ExplainedImage)
async def submit_image(
    echo_id: UUID,
    file: UploadFile = File(...),
    info_in_file_name: bool = False,
    explained_image_dao: ExplainedImageDAO = Depends(),
    echo_dao: EchoDAO = Depends(),
) -> Response:
    """
    Receive an image and process it.
    """
    image_service = ImageService()

    await image_service.save_image(echo_id, explained_image_dao,
                                   echo_dao, file, info_in_file_name)
    return Response(status_code=200)


@router.get("/echo/{echo_id}")
async def get_all(echo_id: UUID, explained_image_dao: ExplainedImageDAO = Depends()):
    images = await explained_image_dao.get_all_explained_images_by_echo_id(echo_id)
    images = [ExplainedImage(image) for image in images]
    return images


@router.get("/image/{image_id}")
async def get_by_id(image_id: UUID, explained_image_dao: ExplainedImageDAO = Depends()):
    image = await explained_image_dao.get_explained_image_by_id(image_id)
    image = ExplainedImage(image)
    return image


@router.delete("/{id}")
async def delete_by_id(id: int, explained_image_dao: ExplainedImageDAO = Depends(), ):
    await explained_image_dao.delete_explained_image_by_id(id)
    return Response(status_code=200)


@router.put("/{id}")
async def update_by_id(image: UpdateExplainedImageDTO,
                       explained_image_dao: ExplainedImageDAO = Depends()):
    print("Updating image")
    await explained_image_dao.update_explained_image_by_id(image)
    return Response()
