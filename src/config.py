import dataclasses
from path_definitions import ROOT
import os

from  dotenv import dotenv_values


mode = os.getenv("MODE", "test")

def env_vals(mode: str):
    match mode:
        case "dev": vals = dotenv_values(f"{ROOT / '.env.dev'}")
        case "test": vals = dotenv_values(f"{ROOT / '.env.test'}")
        case "prod": vals = dotenv_values(f"{ROOT / '.env.prod'}")
        case _: vals = dotenv_values(f"{ROOT / '.env.test'}")
    return vals


@dataclasses.dataclass
class Config:
    db_url = (f"postgresql://{env_vals(mode=mode).get('POSTGRES_USER')}:"
              f"{env_vals(mode=mode).get('POSTGRES_PASSWORD')}@"
              f"{env_vals(mode=mode).get('POSTGRES_HOST')}:"
              f"{env_vals(mode=mode).get('POSTGRES_PORT')}/"
              f"{env_vals(mode=mode).get('POSTGRES_DB')}")
    mode = mode
    env_file = env_vals(mode=mode).get("ENV_FILE")


settings = Config()
