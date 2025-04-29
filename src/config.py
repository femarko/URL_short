import os

from dataclasses import dataclass, field
from  dotenv import load_dotenv


load_dotenv()



@dataclass
class Config:
    """
    Application configuration holder.

    Loads environment variables and assembles a PostgreSQL connection string
    depending on the current runtime mode. This configuration is meant to be
    instantiated once at startup and used throughout the application.

    Attributes
    ----------
    mode : str
        The runtime mode of the application. Can be "prod" or "dev".
    db_url : str
        Fully constructed async PostgreSQL connection URL.
    """
    mode: str = field(default_factory=lambda: os.getenv("MODE", "prod"))
    db_url: str = field(init=False)

    def __post_init__(self):
        """
        Builds the database URL from environment variables after initialization.
        """

        user = os.getenv("POSTGRES_USER")
        password = os.getenv("POSTGRES_PASSWORD")
        host = os.getenv("POSTGRES_HOST")
        port = os.getenv("POSTGRES_PORT")
        database = os.getenv("POSTGRES_DB")

        if not all([user, password, host, port, database]):
            missing = [name for name, value in [
                ("POSTGRES_USER", user),
                ("POSTGRES_PASSWORD", password),
                ("POSTGRES_HOST", host),
                ("POSTGRES_PORT", port),
                ("POSTGRES_DB", database),
            ] if not value]
            raise EnvironmentError(f"Missing environment variables: {', '.join(missing)}")
        self.db_url = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"


settings = Config()
