from fastapi import APIRouter
from app.model.groupchat import GroupChat
from app.services.groupchat import add_group_chat, get_user_gc

router = APIRouter()


@router.post("/store_gc")
def store_gc_to_db(group_chat: GroupChat):
    add_group_chat(group_chat=group_chat)


@router.get("/get_all_gc")
def get_all_gc(username: str):
    users_gc = get_user_gc(username=username)
    return users_gc
