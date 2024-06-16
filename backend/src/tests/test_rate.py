"""Unit testcases for rate calculator API"""

import pytest
from .test_base import client, app, db_session


@pytest.mark.asyncio
async def test_rate_no_param(client):
    """
    Test case to ensure the API returns a 422 status code when no parameters are provided.
    """
    response = client.get("/rates")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_rate_invalid_port(client):
    """
    Test case to ensure the API returns a 404 status code when
    an invalid origin or destination port code is provided.
    """
    response = client.get(
        "/rates?date_from=2016-01-10&date_to=2016-01-11&origin=CNX9AM&destination=NOTAE"
    )
    assert response.status_code == 404
    assert response.json() == {
        "status_code": 404,
        "message": "Invalid input data, more information in details",
        "details": ["Origin port code or slug name provided CNX9AM is not valid"],
    }


@pytest.mark.asyncio
async def test_rate_invalid_date(client):
    """
    Test case to ensure the API returns a 404 status code when an invalid date format is provided.
    """
    response = client.get(
        "/rates?date_from=2016-01-10&date_to=2016-21-21&origin=CNXAM&destination=NOTAE"
    )
    assert response.status_code == 404
    assert response.json() == {
        "status_code": 404,
        "message": "Invalid input data, more information in details",
        "details": ["Invalid date format. Use YYYY-MM-DD format."],
    }


@pytest.mark.asyncio
async def test_rate_invalid_date_range(client):
    """
    Test case to ensure the API returns a 404 status code when an invalid date format is provided.
    """
    response = client.get(
        "/rates?date_from=2016-01-10&date_to=2016-01-01&origin=CNXAM&destination=NOTAE"
    )
    assert response.status_code == 404
    assert response.json() == {
        "status_code": 404,
        "message": "Invalid input data, more information in details",
        "details": ["date_from must be earlier than or equal to date_to"],
    }


@pytest.mark.asyncio
async def test_rate(client):
    """
    Test case to ensure the API returns the correct response with valid parameters.
    """
    response = client.get(
        "/rates?date_from=2016-01-10&date_to=2016-01-11&origin=CNXAM&destination=NOTAE"
    )
    assert response.status_code == 200
    assert response.json() == [
        {"day": "2016-01-10", "average_price": None},
        {"day": "2016-01-11", "average_price": None},
    ]
