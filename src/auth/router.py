from fastapi import APIRouter, Response
from src.core.deps import SessionDep
from src.auth.deps import RefreshTokensDep
from src.auth.schemas import AddUserSchema, LoginUserSchema, UserSchema
import src.auth.crud as crud
from src.auth.utils import generate_tokens
from src.auth.deps import UserDep, AdminUserDep


router = APIRouter(prefix="/api/v1/auth", tags=["Авторизация"])


@router.post("/register", summary="Зарегистрироваться")
async def register(
    user_data: AddUserSchema, response: Response, db: SessionDep
) -> UserSchema:
    user = await crud.create_user(user_data, db)
    generate_tokens({"sub": user.id}, response)
    return user


@router.post("/login", summary="Войти в систему")
async def login(
    user_data: LoginUserSchema, response: Response, db: SessionDep
) -> UserSchema:
    user = await crud.authenticate(user_data, db)
    d = generate_tokens({"sub": user.id}, response)
    print(d["access_token"])
    return user


@router.post("/logout", summary="Выйти из системы")
async def logout(
    response: Response,
):
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return {"message": "Вы вышли из системы"}


@router.post("/refresh", summary="Обновить токены")
async def refresh(tokens: RefreshTokensDep):
    return tokens


@router.post("/profile", summary="Профиль")
async def get_profile(user: UserDep, db: SessionDep) -> UserSchema:
    return await crud.get_profile(user, db)
