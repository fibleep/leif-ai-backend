from pydantic import BaseModel


class EchoDTO(BaseModel):
    name: str
