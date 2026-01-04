from ninja import Router
from django.contrib.auth import get_user_model
from ninja.errors import HttpError
from django.contrib.auth.hashers import make_password, check_password
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from .schemas import UserIn, UserOut, LoginIn, TokenOut

router = Router(tags=["Users"])
User = get_user_model()

@router.post("/register", response=UserOut)
def register(request, payload: UserIn):
    user = User.objects.create(
        username=payload.username,
        email=payload.email,
        password=make_password(payload.password)
    )
    return user


@router.post("/login", response=TokenOut)
def login(request, payload: LoginIn):
    try:
        user = User.objects.get(username=payload.username)
    except User.DoesNotExist:
        raise HttpError(401, "Invalid credentials")

    if not check_password(payload.password, user.password):
        raise HttpError(401, "Invalid credentials")

    token = jwt.encode(
        {
            "user_id": user.id,
            "exp": datetime.utcnow() + timedelta(days=1)
        },
        settings.SECRET_KEY,
        algorithm="HS256"
    )
    return {"access_token": token}