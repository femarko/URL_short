import os

import pytest
from dotenv import dotenv_values

from src.config import Config
from path_definitions import ROOT


def test_settings_with_test_mode():
    settings = Config(mode=os.getenv("MODE"))
    assert settings.db_url == (f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:"
                               f"{os.getenv('POSTGRES_PASSWORD')}@"
                               f"{os.getenv('POSTGRES_HOST')}:"
                               f"{os.getenv('POSTGRES_PORT')}/"
                               f"{os.getenv('POSTGRES_DB')}")
