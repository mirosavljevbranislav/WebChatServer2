from fastapi import APIRouter
from app.services.user import get_user

router = APIRouter()


@router.get('/get_user')
def get_user(username: str):
    user = get_user(username=username)
    return user
