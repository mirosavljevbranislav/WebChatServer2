from fastapi import APIRouter
from app.services.globalchat import store_global_messages, load_global_messages

router = APIRouter()


@router.post("/store_global_messages")
def store_global_messages(message: str):
    store_global_messages(message=message)


@router.get("/get_global_messages")
def get_global_messages():
    messages = load_global_messages()
    return messages
