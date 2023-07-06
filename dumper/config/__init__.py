from pathlib import Path

from pydantic import IPvAnyAddress, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).parent.parent.parent
APP_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(f"{ROOT_DIR}/.env", f"{ROOT_DIR}/.env.prod", f"{ROOT_DIR}/.prod.env")
    )
    debug_mode: bool = True

    # database secrets
    db_username: SecretStr
    db_pwd: SecretStr
    db_tns: SecretStr
    db_host: IPvAnyAddress
    db_port: int
    db_sid: str


settings = Settings()  # type: ignore
