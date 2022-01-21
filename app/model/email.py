from pydantic import BaseModel


class EmailContent(BaseModel):
    recipient: str
    recovery_token: str
