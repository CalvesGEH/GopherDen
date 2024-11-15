import secrets
from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

def determine_secrets(data_dir: Path, production: bool) -> str:
    if not production:
        return "shh-secret-test-key"

    secrets_file = data_dir.joinpath(".secret")
    if secrets_file.is_file():
        with open(secrets_file) as f:
            return f.read()
    else:
        data_dir.mkdir(parents=True, exist_ok=True)
        with open(secrets_file, "w") as f:
            new_secret = secrets.token_hex(32)
            f.write(new_secret)
        return new_secret


class AppSettings(BaseSettings):
    PRODUCTION: bool
    BASE_URL: str = "http://localhost:3000"
    """trailing slashes are trimmed (ex. `http://localhost:8080/` becomes ``http://localhost:8080`)"""

    API_HOST: str = "0.0.0.0"
    API_PORT: int = 7877

    SECRET: str

    TOKEN_TIME: int = 3600

    LOG_CONFIG_OVERRIDE: Path | None = None
    """path to custom logging configuration file"""
    LOG_LEVEL: str = "info"
    """corresponds to standard Python log levels"""

    _DEFAULT_EMAIL: str = "changeme@example.com"
    """
    This is the default email used for the first user created in the database. This is only used if no users
    exist in the database. it should no longer be set by end users.
    """
    _DEFAULT_PASSWORD: str = "MyPassword"
    """
    This is the default password used for the first user created in the database. This is only used if no users
    exist in the database. it should no longer be set by end users.
    """

    @field_validator("BASE_URL")
    @classmethod
    def remove_trailing_slash(cls, v: str) -> str:
        if v and v[-1] == "/":
            return v[:-1]

        return v

    # ===============================================
    # Database Configuration
    DB_ENGINE: str = "sqlite"
    # SQlite database configuration
    SQLITE_DB_NAME: str = "gopherden.db"
        
    # ===============================================
    # Testing Config
    IS_DEMO: bool = False
    TESTING: bool = False


def app_settings_constructor(data_dir: Path, production: bool, env_file: Path, env_encoding="utf-8") -> AppSettings:
    """
    app_settings_constructor is a factory function that returns an AppSettings object. It is used to inject the
    required dependencies into the AppSettings object and nested child objects. AppSettings should not be substantiated
    directly, but rather through this factory function.
    """
    app_settings = AppSettings(
        _env_file=env_file,  # type: ignore
        _env_file_encoding=env_encoding,  # type: ignore
        **{"SECRET": determine_secrets(data_dir, production)},
    )

    return app_settings
