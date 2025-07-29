# app/core/config.py
from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT


class Settings(BaseModel):
    authjwt_secret_key: str = "super_secret_key_123"  # ideal: din .env


@AuthJWT.load_config
def get_config():
    return Settings()
