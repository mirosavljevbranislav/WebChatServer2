from fastapi import FastAPI

from .authentication import router as auth_router
from .groupchat import router as gc_router
from .user import router as user_router


def configure_routers(app: FastAPI):
    """
    Attach routers to the provided FastAPI application
    :param app: instance of FastAPI app to attach routers to
    """
    app.include_router(auth_router)
    app.include_router(gc_router)
    app.include_router(user_router)
