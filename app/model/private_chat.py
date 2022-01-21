from pydantic import BaseModel, Field


class PrivateChatModel(BaseModel):
    id: str = Field(alias="_id")
    participants: list
    messages: list

class PrivateChatSchema(BaseModel):
    participants: list
    messages: list
