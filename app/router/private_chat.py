from fastapi import APIRouter
from app.services.private_chat import PrivateChatSchema
from app.services.private_chat import store_private_chat_to_db, get_private_chat_from_db, store_messages_to_db, load_messages

router = APIRouter()


@router.get("/get_private_chat")
def get_private_chat(username: str, friend: str):
    chat = get_private_chat_from_db(username=username, friend=friend)
    return chat


@router.post("/store_private_chat")
def store_private_chat(private_chat: PrivateChatSchema):
    chat = store_private_chat_to_db(private_chat=private_chat)
    return chat


@router.put("/store_private_messages")
def store_messages(chat_id: str, message: str):
    store_messages_to_db(chat_id=chat_id, message=message)


@router.get("/get_private_messages")
def get_messages(chat_id: str):
    chat_messages = load_messages(chat_id=chat_id)
    return chat_messages
