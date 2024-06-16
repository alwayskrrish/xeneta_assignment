"""Configuration file for Fast API"""

from decouple import Choices, config as get_env

# Toggles debug mode
DEBUG: bool = get_env("DEBUG", cast=bool, default=False)

# Sets the base log level of the application. Defaults to INFO unless RDB_DEBUG is True.
LOG_LEVEL: str = get_env(
    "LOG_LEVEL",
    cast=Choices(["DEBUG", "INFO", "WARNING", "ERROR"]),
    default="DEBUG" if DEBUG else "INFO",
)

# The host ip to bind the application to.
HOST: str = get_env("HOST", default="0.0.0.0")
# The port to bind the application to
PORT: int = get_env("PORT", cast=int, default=8080)

# The Database configurations information to connect
DB_HOSTNAME: str = get_env("DB_HOSTNAME", default="127.0.0.1")
DB_PORT: int = get_env("DB_PORT", cast=int, default=5400)
DB_DATABASE: str = get_env("DB_DATABASE", default="postgres")
DB_USERNAME: str = get_env("DB_USERNAME", default="postgres")
DB_PASSWORD: str = get_env("DB_PASSWORD", default="ratestask")
