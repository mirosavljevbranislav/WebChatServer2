from pydantic import BaseModel


class GroupChat(BaseModel):
    messages: list
