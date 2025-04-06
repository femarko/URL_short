from src.config import env_vals, settings

fake_mode = "test"

def test_env_vals():
    assert env_vals(mode=fake_mode).get("POSTGRES_USER") == "postgres"
    assert env_vals(mode=fake_mode).get("POSTGRES_PASSWORD") == "postgres"
    assert env_vals(mode=fake_mode).get("POSTGRES_HOST") == "localhost"
    assert env_vals(mode=fake_mode).get("POSTGRES_PORT") == "5434"
    assert env_vals(mode=fake_mode).get("POSTGRES_DB") == "test_db"
    assert env_vals(mode=fake_mode).get("ENV_FILE") == ".env.test"


def test_settings():
    assert settings.db_url == "postgresql://postgres:postgres@localhost:5434/test_db"
    assert settings.mode == fake_mode
    assert settings.env_file == ".env.test"