"""FastAPI web application server for Rate Calculator"""

from argparse import Namespace
from logging import getLogger
from time import time

from fastapi import FastAPI, Request

from .routes import root
from . import __version__
from .db import database

LOG = getLogger("rate_calculator")

# Metadata for API documentation
tags_metadata = [
    {
        "name": "Rate",
        "description": "This API is used to get the rates for a specified time period",
    }
]


async def request_timing_middleware(request: Request, call_next):
    """
    Middleware to calculate and log the response time in debug mode.

    Parameters:
    request (Request): The incoming request object
    call_next: The next callable to be executedd
    """
    start_time = time()
    response = await call_next(request)
    LOG.debug("Response time: %.3fs", time() - start_time)
    return response


class RateCalculator:
    """
    Rate calculator class to initiate the FastAPI framework and manage the application.
    """

    def __init__(self, flags: Namespace, db_connection_string: str):
        """
        Initializes the FastAPI application and configures the database connection.

        Parameters:
        flags (Namespace): Command line arguments or configuration flags
        db_connection_string (str): Database connection string
        """
        self._db_connection_string = db_connection_string
        self._flags = flags
        self.app = FastAPI(
            title="Rate Calculator API",
            version=__version__,
            description="This API fetches the rates for a specified date range",
            debug=flags.debug,
            openapi_tags=tags_metadata,
        )
        # Include the routes
        self.app.include_router(root)
        # Add startup and shutdown event handlers
        self.app.add_event_handler("startup", self._startup)
        self.app.add_event_handler("shutdown", self._shutdown)
        # Add request timing middleware in debug mode
        if flags.debug:
            self.app.middleware("http")(request_timing_middleware)

    async def _startup(self):
        """
        Startup event handler to configure the database.
        """
        LOG.debug("Startup signal received")
        database.configure(self._db_connection_string)
        if self._flags.debug:
            LOG.debug("Request timing logging middleware enabled in debug mode")

    async def _shutdown(self):
        """
        Shutdown event handler to dispose the database connection.
        """
        LOG.debug("Shutdown signal received")
        await database.engine.dispose()
