from app.services import groups_db

from app.model.groupchat import GroupChat
from uuid import uuid4


def get_group(group_id: str):
    group = groups_db.find_one({"_id": group_id})
    return group


def add_group_chat(group_chat: GroupChat):
    """
    Stores group chat to database and adds admin to user list
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


def add_user_to_chat(group_id: str, username: str):
    chat = get_group(group_id=group_id)
    if username not in chat['users']:
        groups_db.update_one({"_id": group_id},
                             {"$push": {"users": username}})


def remove_group_chat(group_id: str):
    groups_db.delete_one({"_id": group_id})


def store_messages_to_db(group_id: str, message: str):
    groups_db.update_one({"_id": group_id},
                         {"$push": {"messages": message}})


def load_messages(group_id: str):
    messages = groups_db.find_one({"_id": group_id})
    return messages['messages']
