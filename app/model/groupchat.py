from pydantic import BaseModel, Field


class GroupChat(BaseModel):
    _id: str = Field(alias="_id")
    admin: str
    name: str
    description: str
    users: list
    messages: list
