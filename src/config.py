import dataclasses

from path_definitions import ROOT, TEST_DB
import os

from  dotenv import load_dotenv
load_dotenv()
mode = os.getenv("MODE", "prod")
#
# load_dotenv(f'{ROOT}/.env.{mode}')



@dataclasses.dataclass
class Config:
    def __init__(self, mode: str):
        self.mode = mode
        # self.vals = dotenv_values(f'{ROOT}/.env.{mode}')
        # self.env_file = self.vals.get("ENV_FILE")
        self.db_url = (f"postgresql+asyncpg://"
                f"{os.getenv('POSTGRES_USER')}:"
                f"{os.getenv('POSTGRES_PASSWORD')}@"
                f"{os.getenv('POSTGRES_HOST')}:"
                f"{os.getenv('POSTGRES_PORT')}/"
                f"{os.getenv('POSTGRES_DB')}" )


settings = Config(mode=mode)
