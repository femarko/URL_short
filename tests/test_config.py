from src.config import env_vals, settings
from dotenv import dotenv_values

from path_definitions import ROOT

envfile_values = dotenv_values(ROOT / ".env.test")
fake_mode = "test"

def test_env_vals():
    assert env_vals(mode=fake_mode).get("POSTGRES_USER") == envfile_values.get("POSTGRES_USER")
    assert env_vals(mode=fake_mode).get("POSTGRES_PASSWORD") == envfile_values.get("POSTGRES_PASSWORD")
    assert env_vals(mode=fake_mode).get("POSTGRES_HOST") == envfile_values.get("POSTGRES_HOST")
    assert env_vals(mode=fake_mode).get("POSTGRES_PORT") == envfile_values.get("POSTGRES_PORT")
    assert env_vals(mode=fake_mode).get("POSTGRES_DB") == envfile_values.get("POSTGRES_DB")
    assert env_vals(mode=fake_mode).get("ENV_FILE") == envfile_values.get("ENV_FILE")


def test_settings():
    assert settings.db_url == (f"postgresql://{envfile_values.get('POSTGRES_USER')}:"
                               f"{envfile_values.get('POSTGRES_PASSWORD')}@"
                               f"{envfile_values.get('POSTGRES_HOST')}:"
                               f"{envfile_values.get('POSTGRES_PORT')}/"
                               f"{envfile_values.get('POSTGRES_DB')}")
    assert settings.mode == fake_mode
    assert settings.env_file == envfile_values.get("ENV_FILE")