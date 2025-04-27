import os

from src.config import Config


def test_settings_with_test_mode():
    settings = Config(mode=os.getenv("MODE"))
    assert settings.db_url == (f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:"
                               f"{os.getenv('POSTGRES_PASSWORD')}@"
                               f"{os.getenv('POSTGRES_HOST')}:"
                               f"{os.getenv('POSTGRES_PORT')}/"
                               f"{os.getenv('POSTGRES_DB')}")
