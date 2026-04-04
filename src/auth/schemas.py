from pydantic import BaseModel, EmailStr, Field, model_validator
from datetime import datetime


class AddUserSchema(BaseModel):
    username: str = Field(..., min_length=5, description="Введите логин пользователя")
    email: EmailStr = Field(..., min_length=5, description="Введите почту пользователя")
    password: str = Field(..., min_length=5, description="Введите пароль пользователя")
    confirm_password: str = Field(
        ..., min_length=5, description="Повторите пароль пользователя"
    )

    @model_validator(mode="after")
    def verify_password(self) -> "AddUserSchema":
        if self.password != self.confirm_password:
            raise ValueError(["Пароли не совпадают"])
        return self


class LoginUserSchema(BaseModel):
    login: str = Field(..., description="Введите почту или логин пользователя")
    password: str = Field(..., description="Введите пароль пользователя")


class UserSchema(BaseModel):
    username: str
    email: str
    skills: str | None
    experience_level: str | None
    desired_salary: int | None
    about: str | None
    is_admin: bool
    created_at: datetime
