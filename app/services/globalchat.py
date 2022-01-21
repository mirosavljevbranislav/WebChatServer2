from app.services import global_db


def get_global_id():
    global_chat = global_db.find_one()
    return global_chat


def load_global_messages():
    global_chat_id = get_global_id()
    global_messages = global_db.find_one({"_id": global_chat_id['_id']})
    return global_messages['messages']


def store_global_messages(message: str):
    chat_id = get_global_id()
    global_db.update_one({"_id": chat_id['_id']},
                         {"$push": {"messages": message}})
