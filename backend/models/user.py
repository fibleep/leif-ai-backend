from pydantic import BaseModel
from typing import Optional
from enum import Enum
from dataclasses import dataclass

from backend.models.roles import Role


class NewUser(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True


class ResUser(BaseModel):
    id: int
    fullname: str
    email: str
    role: Role
    date: str
    time: str

    class Config:
        from_attributes = True


class ResUpdateUser(BaseModel):
    id: int
    fullname: str
    email: str
    password: str
    role: Role
    date: str
    time: str

    class Config:
        from_attributes = True


class Login(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True
