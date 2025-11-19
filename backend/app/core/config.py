from typing import Optional
import os
from pydantic_settings import BaseSettings
from pydantic import validator

class Settings(BaseSettings):
    PROJECT_NAME: str = "DevPrepLab"
    PROJECT_VERSION: str = "1.0.0"
    
    ENVIRONMENT: str = "dev"
    TESTING: bool = False

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str
    POSTGRES_DB_TEST: str = "test_devpreplab"

    DATABASE_URL: Optional[str] = None

    TEST_DATABASE_URL: Optional[str] = None

    @validator("POSTGRES_SERVER", pre=True)
    def set_postgres_server(cls, v, values):
        if values.get("ENVIRONMENT") == "dev" and v == "postgres":
            return "localhost"
        return v

    @validator("POSTGRES_PORT", pre=True)
    def set_postgres_port(cls, v, values):
        if values.get("ENVIRONMENT") == "dev" or values.get("TESTING"):
            return 5433
        return v

    @validator("DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict[str, any]) -> any:
        if isinstance(v, str):
            return v
        return f"postgresql://{values.get('POSTGRES_USER')}:{values.get('POSTGRES_PASSWORD')}@{values.get('POSTGRES_SERVER')}:{values.get('POSTGRES_PORT')}/{values.get('POSTGRES_DB')}"

    @validator("TEST_DATABASE_URL", pre=True)
    def assemble_test_db_connection(cls, v: Optional[str], values: dict[str, any]) -> any:
        if isinstance(v, str):
            return v
        print(f"DEBUG: POSTGRES_USER in validator: {values.get('POSTGRES_USER')}")
        print(f"DEBUG: POSTGRES_PASSWORD in validator: {values.get('POSTGRES_PASSWORD')}")
        test_db_url = f"postgresql://{values.get('POSTGRES_USER')}:{values.get('POSTGRES_PASSWORD')}@{values.get('POSTGRES_SERVER')}:{values.get('POSTGRES_PORT')}/test_devpreplab"
        print(f"DEBUG: Constructed TEST_DATABASE_URL: {test_db_url}")
        return test_db_url

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

print(f"DEBUG: Before Settings() - os.environ.get('POSTGRES_USER'): {os.environ.get('POSTGRES_USER')}")
print(f"DEBUG: Before Settings() - os.environ.get('POSTGRES_PASSWORD'): {os.environ.get('POSTGRES_PASSWORD')}")
settings = Settings()
print(f"DEBUG: After Settings() - settings.TEST_DATABASE_URL: {settings.TEST_DATABASE_URL}")
