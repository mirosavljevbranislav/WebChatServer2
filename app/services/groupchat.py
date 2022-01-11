from app.services import app_db

from app.model.groupchat import GroupChat
from .user import get_user
from uuid import uuid4


def add_group_chat(group_chat: GroupChat):
    """
    Creates and adds new group to user's list of group chats
    :param group_chat: model of group chat for storing
    :return: None
    """
    gc_info = group_chat.dict()
    gc_info["_id"] = str(uuid4())

    app_db.update_one({"username": gc_info['admin']},
                      {"$push": {"group_chats": gc_info}})


def get_user_gc(username: str):
    """
    Returns list of users group chats
    :param username: user's username
    :return: list of groups
    """
    user = get_user(username=username)
    users_gc = [gc for gc in user['group_chats']]
    return users_gc
