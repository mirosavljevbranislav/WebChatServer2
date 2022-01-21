from app.model.private_chat import PrivateChatSchema
from uuid import uuid4
from app.services import chat_db


def get_private_chat_from_db(username: str, friend: str):
    all_chats = chat_db.find()
    user_chats = [user for user in all_chats if username in user['participants'] and friend in user['participants']]
    return user_chats


def store_private_chat_to_db(private_chat: PrivateChatSchema):
    private_chat_info = private_chat.dict()
    private_chat_info['_id'] = str(uuid4())
    chat_db.insert_one(private_chat_info)
    return private_chat_info


def store_messages_to_db(chat_id: str, message: str):
    chat_db.update_one({"_id": chat_id},
                       {"$push": {"messages": message}})


def load_messages(chat_id: str):
    messages = chat_db.find_one({"_id": chat_id})
    return messages['messages']
