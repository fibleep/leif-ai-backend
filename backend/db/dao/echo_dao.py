from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.dependencies import get_db_session
from backend.db.models.echo_model import EchoModel
from backend.models.echo import Echo
from backend.web.api.echoes.dtos.echo_dto import EchoDTO


class EchoDAO:
    """Class for creating an echo."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create(self, echo:EchoDTO):

        echo_model = EchoModel(
            name=echo.name
        )
        self.session.add(echo_model)
        await self.session.commit()
        return echo_model

    async def remove(self, echo_id:int):
        echo = await self.session.get(EchoModel, echo_id)
        await self.session.delete(echo)
        await self.session.commit()
        return echo

    async def get(self, echo_id:int):
        echo = await self.session.get(EchoModel, echo_id)
        return echo

    async def get_all(self):
        echoes = await self.session.execute(select(EchoModel))
        return echoes.scalars().all()

    async def update(self, echo_id:int, echo:EchoDTO):
        echo_model = await self.session.get(EchoModel, echo_id)
        echo_model.name = echo.name
        await self.session.commit()
        return echo_model
