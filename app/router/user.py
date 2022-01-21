from fastapi import APIRouter
from app.services.user import get_user_from_db, \
    add_friend_to_db, \
    change_user_password, \
    remove_friend_from_db,\
    check_if_user_in_friends

router = APIRouter()


@router.get('/get_user')
def get_user(username: str):
    user = get_user_from_db(username=username)
    return user


@router.post('/add_friend')
def add_friend(username: str, current_user: str):
    user = add_friend_to_db(username_to_add=username, current_user=current_user)
    return user


@router.put("/restore_password")
def restore_password(updated_info: dict):
    change_user_password(username=updated_info['username'],
                         new_password=updated_info['new_password'])


@router.delete("/remove_friend")
def remove_friend(friend_to_remove: str, username: str):
    remove_friend_from_db(friend_to_remove=friend_to_remove,
                          username=username)


@router.get("/check_user")
def check_user(username: str, friend: str):
    if check_if_user_in_friends(username=username, friend=friend):
        return True
    return False
