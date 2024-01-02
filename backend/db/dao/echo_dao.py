from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.dependencies import get_db_session
from backend.db.models.echo_model import EchoModel


class EchoDAO:
    """Class for creating an echo."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create(self, echo):

        echo_model = EchoModel(
            name=echo.name
        )
        self.session.add(echo_model)
        await self.session.commit()
        return echo_model

    async def remove(self, echo_id:UUID):
        echo = await self.session.get(EchoModel, echo_id)
        await self.session.delete(echo)
        await self.session.commit()
        return echo

    async def get(self, echo_id:UUID):
        echo = await self.session.get(EchoModel, echo_id)
        return echo

    async def get_all(self):
        result = await self.session.execute(
            select(EchoModel)
        )
        return result.scalars().all()

    async def update(self, echo_id:int, echo):
        echo_model = await self.session.get(EchoModel, echo_id)
        echo_model.name = echo.name
        await self.session.commit()
        return echo_model
