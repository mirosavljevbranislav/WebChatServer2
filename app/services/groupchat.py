from app.services import groups_db

from app.model.groupchat import GroupChat
from uuid import uuid4


def add_group_chat(group_chat: GroupChat):
    """
    Creates and adds new group to user's list of group chats
    :param group_chat: model of group chat for storing
    :return: None
    """
    gc_info = group_chat.dict()
    gc_info["_id"] = str(uuid4())

    groups_db.insert_one(gc_info)
    group_id = gc_info['_id']
    gc_admin = gc_info['admin']
    add_user_to_chat(group_id, gc_admin)


def get_user_gc(username: str):
    """
    Returns list of users group chats
    :param username: user's username
    :return: list of groups
    """
    all_groups = groups_db.find()
    user_groups = [group for group in all_groups if username in group['users']]
    return user_groups


def add_user_to_chat(chat_id: str, username: str):
    groups_db.update_one({"_id": chat_id},
                         {"$push": {"users": username}})
