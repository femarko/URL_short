import pytest
from dotenv import dotenv_values


from src.config import Config
from path_definitions import ROOT


@pytest.mark.parametrize("fake_mode", ["dev", "test"])
def test_settings_with_non_test_mode(fake_mode):
    settings = Config(mode=fake_mode)
    envfile_values = dotenv_values(f'{ROOT}/.env.{fake_mode}')
    assert settings.db_url == (f"postgresql+asyncpg://{envfile_values.get('POSTGRES_USER')}:"
                               f"{envfile_values.get('POSTGRES_PASSWORD')}@"
                               f"{envfile_values.get('POSTGRES_HOST')}:"
                               f"{envfile_values.get('POSTGRES_PORT')}/"
                               f"{envfile_values.get('POSTGRES_DB')}")
