from app.services import user_db
from app.services.authentication import get_password_hash

from app.model.user import UserSchema

from uuid import uuid4


def check_if_user_exists(user_username: str):
    """
    Checks if user already exists in database
    :return: true/false
    """
    user = user_db.find_one({"username": user_username})
    if user:
        return True
    return False


def check_if_user_in_friends(username: str, friend: str):
    user = user_db.find_one({"username": username})
    if friend in user['friends']:
        return True
    return False


def store_user(user_data: UserSchema):
    """
    Stores user to database
    :param user_data: user's data
    :return:
    """
    if not check_if_user_exists(user_data.username):
        user_dict = user_data.dict()
        user_dict["_id"] = str(uuid4())
        user_dict["password"] = get_password_hash(user_data.password)
        user_db.insert_one(user_dict)
        print({"Message": "User stored successfully!"})
        return True
    else:
        print({"Message": "Username already in use..."})
        return False


def get_user_from_db(username: str):
    """
    This returns whole user if needed
    :param username:
    :return:
    """
    user = user_db.find_one({"username": username})
    if user:
        return user
    return {"Message": "User not found"}, 404


def add_friend_to_db(username_to_add: str, current_user: str):
    user = get_user_from_db(username=username_to_add)
    if user:
        user_db.update_one({"username": current_user},
                           {"$push": {"friends": username_to_add}})
        user_db.update_one({"username": username_to_add},
                           {"$push": {"friends": current_user}})

        return user
    else:
        return {"Message": "User not found"}


def remove_friend_from_db(friend_to_remove: str, username: str):
    user_db.update_one({"username": username},
                       {"$pull": {"friends": friend_to_remove}})


def change_user_password(username: str, new_password: str):
    hashed_password = get_password_hash(new_password)
    user_db.update_one({"username": username},
                       {"$set": {"password": hashed_password}})
