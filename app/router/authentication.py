from datetime import timedelta

from fastapi import HTTPException, APIRouter
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from starlette import status
from starlette.responses import JSONResponse

from app.model.user import UserSchema
from app.model.token import Token
from app.model.email import EmailContent

from app.services.user import store_user
from app.services.authentication import authenticate_user, create_access_token, get_current_user

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()


@router.post("/login", response_model=Token)
async def login_user(data: dict):
    user = authenticate_user(data['username'], data['password'])
    if not user:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['username']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register")
async def register_user(data: UserSchema):
    if store_user(data):
        return "True"
    else:
        return "False"


@router.get("/get_logged_user/{access_token}")
async def get_logged_user(access_token):
    if access_token:
        user = get_current_user(access_token)
        return user
    else:
        return {"Message": "User none"}


conf = ConnectionConfig(
    MAIL_USERNAME="branislav.mirosavljev01@gmail.com",
    MAIL_PASSWORD="1mirosavljev1",
    MAIL_FROM="branislav.mirosavljev01@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="Desired Name",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True
)


@router.post("/send_mail")
async def simple_send(content: EmailContent):
    recovery_info = content.dict()
    html = f"""Hello {recovery_info['recipient']},
            here is your code to reset your password: {recovery_info['recovery_token']}"""
    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=[f"{recovery_info['recipient']}"],  # List of recipients, as many as you can pass
        body=html,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    return {"status": "ok"}
