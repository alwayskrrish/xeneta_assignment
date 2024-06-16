"""Unit testcases base for rate calculator API"""

from types import SimpleNamespace
from typing import Generator, Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine
from core.app import RateCalculator
from lib.sqla.db import Database
from lib.sqla.db import create_psql_connection_string
import config as cfg


def start_application():
    """
    Create and configure the RateCalculator application instance.
    """
    rdb = RateCalculator(
        SimpleNamespace(debug=False, host="0.0.0.0", port=8080, test=True),
        create_psql_connection_string(
            cfg.DB_USERNAME,
            cfg.DB_PASSWORD,
            cfg.DB_HOSTNAME,
            cfg.DB_DATABASE,
            cfg.DB_PORT,
        ),
    )

    test_app = rdb.app
    return test_app


@pytest.fixture(scope="function", name="app")
def app() -> Generator[FastAPI, Any, None]:
    """
    Pytest fixture to create a fresh FastAPI application instance for each test.
    """
    _app = start_application()
    yield _app


@pytest.fixture(scope="function", name="db_session")
def db_session(test_app: FastAPI):
    """
    Pytest fixture to create a database session for each test.
    """
    # Create an asynchronous engine for the test database
    engine = create_async_engine(
        create_psql_connection_string(
            cfg.DB_USERNAME,
            cfg.DB_PASSWORD,
            cfg.DB_HOSTNAME,
            cfg.DB_DATABASE,
            cfg.DB_PORT,
        )
    )
    return engine.connect()


@pytest.fixture(scope="function", name="client")
def client(test_app: FastAPI, db_session: Database):
    """
    Pytest fixture to create a new FastAPI TestClient that uses the `db_session` fixture
    to override the `get_db` dependency that is injected into routes.
    """

    def get_test_db():
        """
        Dependency override function to use the test database session.
        """
        try:
            return db_session
        finally:
            pass

    with TestClient(test_app) as test_client:
        yield test_client
