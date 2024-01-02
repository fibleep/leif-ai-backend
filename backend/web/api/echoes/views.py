
from uuid import UUID

from fastapi import APIRouter
from fastapi.param_functions import Depends
from starlette.responses import Response


from backend.db.dao.echo_dao import EchoDAO
from backend.web.api.echoes.dtos.echo_dto import EchoDTO

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
    return Response(status_code=201)


@router.get("/")
async def get_all_echoes(
    echo_dao: EchoDAO = Depends(),
):
    """
    Get all echoes
    """
    echoes = await echo_dao.get_all()
    return echoes


@router.delete("/{echo_id}")
async def delete_echo(
    echo_id: UUID,
    echo_dao: EchoDAO = Depends()
):
    await echo_dao.remove(echo_id)
    return Response(status_code=204)
