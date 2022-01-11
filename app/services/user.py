from app.services import app_db
from app.services.authentication import get_password_hash

from app.model.user import UserSchema

from uuid import uuid4


def check_if_user_exists(user_username: str):
    """
    Checks if user already exists in database
    :return: true/false
    """
    user = app_db.find_one({"username": user_username})
    if user:
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
        app_db.insert_one(user_dict)
        print({"Message": "User stored successfully!"})
        return True
    else:
        print({"Message": "Username already in use..."})
        return False


def get_user(username: str):
    """
    This returns whole user if needed
    :param username:
    :return:
    """
    user = app_db.find_one({"username": username})
    if user:
        return user
    return {"Message": "User not found"}, 404
