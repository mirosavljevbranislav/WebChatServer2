from fastapi import FastAPI

from .authentication import router as auth_router
from .groupchat import router as gc_router
from .user import router as user_router
from .private_chat import router as private_chat_router
from .globalchat import router as global_chat_router


def configure_routers(app: FastAPI):
    """
    Attach routers to the provided FastAPI application
    :param app: instance of FastAPI app to attach routers to
    """
    app.include_router(auth_router)
    app.include_router(gc_router)
    app.include_router(user_router)
    app.include_router(private_chat_router)
    app.include_router(global_chat_router)
