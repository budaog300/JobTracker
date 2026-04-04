from jose import jwt, JWTError
from fastapi import Response, Request, Depends
from sqlalchemy import select
from typing import Annotated

from src.core.deps import SessionDep
from src.auth.utils import auth_data, generate_tokens
from src.exceptions import UnauthorizedException, ForbiddenException
from src.core.models import User


async def refresh_tokens(request: Request, response: Response, db: SessionDep):
    token = request.cookies.get("refresh_token")
    if not token:
        raise UnauthorizedException("Token required!")
    try:
        payload = jwt.decode(
            token,
            key=auth_data["refresh_secret_key"],
            algorithms=auth_data["algorithm"],
        )
        if payload.get("type") != "refresh":
            raise UnauthorizedException("Неправильный тип токена!")
        user_id = payload.get("sub")
        if not user_id:
            raise UnauthorizedException("Не найден ID пользователя в токене!")
        query = select(User).where(User.id == user_id)
        user = (await db.execute(query)).scalar_one_or_none()
        if not user or not user.is_active:
            raise UnauthorizedException("Пользователь не найден")
        tokens = generate_tokens({"sub": user_id}, response)
        return {
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
        }
    except JWTError:
        raise UnauthorizedException("Token required!")


async def get_current_user(request: Request, db: SessionDep):
    token = request.cookies.get("access_token")
    # print(token)
    if not token:
        raise UnauthorizedException("Token required!")
    try:
        payload = jwt.decode(
            token, key=auth_data["access_secret_key"], algorithms=auth_data["algorithm"]
        )
        user_id = payload.get("sub")
        if not user_id:
            raise UnauthorizedException("Не найден ID пользователя в токене!")
        query = select(User).where(User.id == user_id)
        user = (await db.execute(query)).scalar_one_or_none()
        if not user or not user.is_active:
            raise UnauthorizedException("Пользователь не найден")
        return user
    except JWTError:
        raise UnauthorizedException("Token required!")


async def get_admin_user(user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise ForbiddenException("Недостаточно прав!")
    return user


UserDep = Annotated[User, Depends(get_current_user)]
AdminUserDep = Annotated[User, Depends(get_admin_user)]
RefreshTokensDep = Annotated[User, Depends(refresh_tokens)]
