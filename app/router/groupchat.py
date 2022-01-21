from fastapi import APIRouter
from app.model.groupchat import GroupChat
from app.services.groupchat import add_group_chat,\
    get_user_gc,\
    add_user_to_chat,\
    remove_group_chat,\
    store_messages_to_db, \
    load_messages

router = APIRouter()


@router.post("/store_gc")
def store_gc_to_db(group_chat: GroupChat):
    add_group_chat(group_chat=group_chat)


@router.get("/get_all_gc")
def get_all_gc(username: str):
    users_gc = get_user_gc(username=username)
    return users_gc


@router.post("/add_user_to_gc")
def store_user_to_gc(user_info: dict):
    add_user_to_chat(group_id=user_info['group_id'],
                     username=user_info['username'])


@router.delete("/remove_gc/{group_id}")
def remove_gc(group_id: str):
    remove_group_chat(group_id=group_id)


@router.put("/store_group_messages")
def store_messages(group_id: str, message: str):
    store_messages_to_db(group_id=group_id, message=message)


@router.get("/get_group_messages")
def get_messages(group_id: str):
    group_messages = load_messages(group_id=group_id)
    return group_messages
