from select import select

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from backend.db.dependencies import get_db_session
from backend.db.models.user_model import UserModel
from sqlalchemy import select


class UserDAO:
    def __init__(self, db_session: AsyncSession = Depends(get_db_session)):
        self.db_session = db_session

    async def save(self, user: UserModel) -> UserModel:
        """
        Create a new user in the database.
        """
        try:
            self.db_session.add(user)
            return user
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            raise e

    async def get_user_by_email(self, email: str) -> UserModel:
        """
        Fetch a single user by email.
        """
        query = await self.db_session.execute(
            select(UserModel).filter(UserModel.email == email)
        )
        return query.scalar()

    async def get_all(self):
        query = await self.db_session.query(UserModel)
        return query.all()
