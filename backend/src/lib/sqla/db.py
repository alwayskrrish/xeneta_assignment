"""Database connectivity"""

from functools import wraps
from logging import getLogger
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine
from sqlalchemy.ext.asyncio.engine import create_async_engine

# Initialize the logger
LOG = getLogger(__name__)


def require_configured(fn):
    """
    Decorator to ensure the database engine is configured before executing the function
    """

    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        if self.engine is None:
            raise RuntimeError("Database engine not yet configured")
        return fn(self, *args, **kwargs)

    return wrapper


def create_psql_connection_string(
    username: str,
    password: str,
    hostname: str,
    database: str,
    port: Optional[int] = 5432,
) -> str:
    """
    Returns the PostgreSQL connection string.

    Parameters:
    username (str): Database username
    password (str): Database password
    hostname (str): Database hostname
    database (str): Database name
    port (Optional[int]): Database port, default is 5432

    Returns:
    str: The connection string for PostgreSQL
    """
    return f"postgresql+asyncpg://{username}:{password}@{hostname}:{port}/{database}"


class Database:
    """
    Database class to maintain database connection
    """

    def __init__(self) -> None:
        self.engine: Optional[AsyncEngine] = None

    def configure(self, connection_string: str):
        """
        Configures the database engine with the given connection string.

        Parameters:
        connection_string (str): The connection string for the database
        """
        kwargs = {}

        self.engine: AsyncEngine = create_async_engine(connection_string, **kwargs)
        LOG.debug("Database connection configured")

    @require_configured
    def begin(self, *args, **kwargs) -> AsyncConnection:
        """
        Convenience method for AsyncEngine.begin()

        Returns:
        AsyncConnection: The asynchronous connection object
        """
        return self.engine.begin(*args, **kwargs)

    @require_configured
    def connect(self, *args, **kwargs) -> AsyncConnection:
        """
        Convenience method for AsyncEngine.connect()

        Returns:
        AsyncConnection: The asynchronous connection object
        """
        return self.engine.connect(*args, **kwargs)

    def __call__(self) -> "Database":
        """
        Make the Database object callable, as per FastAPI dependency injection mechanism.

        Returns:
        Database: The database object itself
        """
        return self

    def __repr__(self) -> str:
        """
        String representation of the Database object.

        Returns:
        str: The name of the database engine
        """
        return f"Database<{self.engine.name}>"
