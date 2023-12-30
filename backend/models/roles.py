from enum import Enum


class Role(str, Enum):
    USER = "user"
    MANAGER = "manager"
    ADMIN = "admin"
