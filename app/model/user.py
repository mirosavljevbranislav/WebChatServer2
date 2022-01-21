from pydantic import BaseModel, Field


class UserModel(BaseModel):
    id: str = Field(alias="_id")
    username: str
    password: str
    full_name: str
    last_name: str
    email: str
    friends: list


class UserSchema(BaseModel):
    username: str
    password: str
    full_name: str
    last_name: str
    email: str
    friends: list
