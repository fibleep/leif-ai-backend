from tokenize import String
from typing import Any


from sqlalchemy import Column, Integer, String, Text, Enum, UUID

from backend.db.base import Base


class UserModel(Base):
    __tablename__ = 'users'
    id = Column(UUID, primary_key=True, autoincrement=True)
    email = Column(Text, nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role = Column(Enum('ADMIN', 'USER', name='role_type'), nullable=False, default='USER')
