import dataclasses

from path_definitions import ROOT, TEST_DB
import os

from  dotenv import dotenv_values


mode = os.getenv("MODE", "test")


@dataclasses.dataclass
class Config:
    def __init__(self, mode: str):
        self.mode = mode
        self.vals = dotenv_values(f'{ROOT}/.env.{mode}')
        self.env_file = self.vals.get("ENV_FILE")
        self.db_url = (f"postgresql+asyncpg://"
                f"{self.vals.get('POSTGRES_USER')}:"
                f"{self.vals.get('POSTGRES_PASSWORD')}@"
                f"{self.vals.get('POSTGRES_HOST')}:"
                f"{self.vals.get('POSTGRES_PORT')}/"
                f"{self.vals.get('POSTGRES_DB')}" )


settings = Config(mode=mode)
