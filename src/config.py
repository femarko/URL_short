import dataclasses
import os

from  dotenv import load_dotenv


load_dotenv()
mode = os.getenv("MODE", "prod")


@dataclasses.dataclass
class Config:
    """
    Configuration of the application.

    This class stores the configuration of the application.
    The configuration is set up based on the value of the
    `MODE` environment variable.

    Attributes
    ----------
    mode : str
        The mode of the application. Can be either "prod" or "dev".
    db_url : str
        The URL of the database.
    """
    def __init__(self, mode: str):
        self.mode = mode
        self.db_url = (f"postgresql+asyncpg://"
                f"{os.getenv('POSTGRES_USER')}:"
                f"{os.getenv('POSTGRES_PASSWORD')}@"
                f"{os.getenv('POSTGRES_HOST')}:"
                f"{os.getenv('POSTGRES_PORT')}/"
                f"{os.getenv('POSTGRES_DB')}" )


settings = Config(mode=mode)
