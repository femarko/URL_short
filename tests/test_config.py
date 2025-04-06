from src.config import settings
from dotenv import dotenv_values

from path_definitions import ROOT


def test_settings():
    fake_mode = "dev"
    envfile_values = dotenv_values(f'{ROOT}/.env.{fake_mode}')
    assert settings.mode == fake_mode
    assert settings.db_url == (f"postgresql://{envfile_values.get('POSTGRES_USER')}:"
                               f"{envfile_values.get('POSTGRES_PASSWORD')}@"
                               f"{envfile_values.get('POSTGRES_HOST')}:"
                               f"{envfile_values.get('POSTGRES_PORT')}/"
                               f"{envfile_values.get('POSTGRES_DB')}")
    assert settings.env_file == envfile_values.get("ENV_FILE")
