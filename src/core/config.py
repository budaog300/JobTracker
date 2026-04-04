from pydantic_settings import BaseSettings, SettingsConfigDict


class SettingDB(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    model_config = SettingsConfigDict(env_file=".env.db", extra="ignore")

    @property
    def get_db_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class SettingAuth(BaseSettings):
    ACCESS_SECRET_KEY: str
    REFRESH_SECRET_KEY: str
    ALGORITHM: str

    model_config = SettingsConfigDict(env_file=".env.auth", extra="ignore")

    @property
    def get_auth_data(self) -> dict:
        return {
            "access_secret_key": self.ACCESS_SECRET_KEY,
            "refresh_secret_key": self.REFRESH_SECRET_KEY,
            "algorithm": self.ALGORITHM,
        }


class SettingAI(BaseSettings):
    OPENAI_API_KEY: str
    BASE_URL: str

    model_config = SettingsConfigDict(env_file=".env.ai", extra="ignore")

    @property
    def get_api_key(self) -> dict:
        return {"API_KEY": self.OPENAI_API_KEY, "BASE_URL": self.BASE_URL}


db_settings = SettingDB()
auth_settings = SettingAuth()
ai_settings = SettingAI()
