from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, or_, and_

from src.core.models import User
from src.auth.schemas import AddUserSchema, LoginUserSchema, UserSchema
from src.exceptions import ItemAlreadyExistException, UnauthorizedException


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_passwor_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hash_password: str) -> bool:
    return pwd_context.verify(password, hash_password)


async def create_user(user_data: AddUserSchema, db: AsyncSession) -> UserSchema:
    query = select(User).where(
        or_(
            User.email == user_data.email,
            User.username == user_data.username,
        )
    )
    try:
        res = await db.execute(query)
        result = res.scalars().first()
        if not result:
            user = user_data.model_dump(exclude={"confirm_password"})
            user["password"] = get_passwor_hash(user["password"])
            new_user = User(**user)
            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)
            return new_user
        raise ItemAlreadyExistException(
            "Пользователь с таким email или username уже существует"
        )
    except Exception as e:
        await db.rollback()
        raise e


async def authenticate(user_data: LoginUserSchema, db: AsyncSession) -> UserSchema:
    query = select(User).where(
        and_(
            or_(User.username == user_data.login, User.email == user_data.login),
            User.is_active == True,
        )
    )
    try:
        res = await db.execute(query)
        user = res.scalar_one_or_none()
        if not user or not verify_password(user_data.password, user.password):
            raise UnauthorizedException("Неверный логин или пароль!")
        return user
    except Exception as e:
        raise e


async def get_profile(user: User, db: AsyncSession) -> UserSchema:
    query = select(User).where(User.id == user.id)
    try:
        user = (await db.execute(query)).scalar_one_or_none()
        return user
    except Exception as e:
        raise e
