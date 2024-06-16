"""Rate calculator API"""

from argparse import ArgumentParser
from uvicorn import run

from core import __version__
from core.app import RateCalculator
from lib.log import get_config
from lib.sqla.db import create_psql_connection_string

import config as cfg

if __name__ == "__main__":
    parser = ArgumentParser(
        "Rate Calculator", description="Rate Calculator backend application"
    )

    # Add debug option to enable debug logging
    parser.add_argument(
        "-d",
        "--debug",
        help="enable debug options and logging",
        action="store_true",
    )

    # Add host argument to specify the listening address
    parser.add_argument(
        "--host", help="the listening address to bind to", default=cfg.HOST
    )

    # Add port argument to specify the listening port
    parser.add_argument(
        "--port",
        help="the listening port to bind to",
        type=int,
        default=cfg.PORT,
    )

    # Add version argument to display the version information
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"Rate Calculator v{__version__}",
        help="show version information and exit",
    )

    # Parse command line arguments
    flags = parser.parse_args()

    # Create RateCalculator instance with the parsed flags and database connection string
    rc = RateCalculator(
        flags,
        create_psql_connection_string(
            cfg.DB_USERNAME,
            cfg.DB_PASSWORD,
            cfg.DB_HOSTNAME,
            cfg.DB_DATABASE,
            cfg.DB_PORT,
        ),
    )

    # Configure logging based on the debug flag
    log_config = get_config(log_level="DEBUG" if flags.debug else cfg.LOG_LEVEL)

    # Run the FastAPI application using Uvicorn
    run(
        rc.app,
        host=flags.host,
        port=flags.port,
        log_config=log_config,
    )
