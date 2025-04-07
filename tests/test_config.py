import pytest

from src.config import Config
from dotenv import dotenv_values

from path_definitions import ROOT, TEST_DB


def test_settings_with_test_mode():
    fake_mode = "test"
    settings = Config(mode=fake_mode)
    envfile_values = dotenv_values(f'{ROOT}/.env.{fake_mode}')
    assert settings.mode == fake_mode
    assert settings.db_url == f"sqlite:///{TEST_DB}"
    assert settings.env_file == envfile_values.get("ENV_FILE")


@pytest.mark.parametrize("fake_mode", ["dev"])
def test_settings_with_non_test_mode(fake_mode):
    settings = Config(mode=fake_mode)
    envfile_values = dotenv_values(f'{ROOT}/.env.{fake_mode}')
    assert settings.db_url == (f"postgresql://{envfile_values.get('POSTGRES_USER')}:"
                               f"{envfile_values.get('POSTGRES_PASSWORD')}@"
                               f"{envfile_values.get('POSTGRES_HOST')}:"
                               f"{envfile_values.get('POSTGRES_PORT')}/"
                               f"{envfile_values.get('POSTGRES_DB')}")
