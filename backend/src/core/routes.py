"""Component API routers"""

from datetime import datetime
from logging import getLogger
from typing import Dict, Any, List

import asyncpg
from fastapi import APIRouter, Depends, HTTPException

from .db import Database, database
from .response_model import response_error
from .crud import get_average_prices, get_port_codes
from .model import PriceResponse

root = APIRouter()

LOG = getLogger("rate_calculator")


async def validate_dates(date_from: str, date_to: str) -> str:
    """
    Validate the date format and ensure date_from is earlier than date_to.

    Args:
        date_from (str): The start date in YYYY-MM-DD format.
        date_to (str): The end date in YYYY-MM-DD format.

    Returns:
        str: An error message if validation fails, otherwise None.
    """
    try:
        # Parse the date strings into datetime objects
        date_from = datetime.strptime(date_from, "%Y-%m-%d")
        date_to = datetime.strptime(date_to, "%Y-%m-%d")

        # Check if date_from is earlier than date_to
        if date_from > date_to:
            return "date_from must be earlier than or equal to date_to"

        return None
    except ValueError:
        # Return an error if date strings are not in the correct format
        return "Invalid date format. Use YYYY-MM-DD format."


@root.get(
    "/rates",
    tags=["Rate"],
    response_model=List[PriceResponse],
    summary="Get Average Prices",
    description="Fetch avg price for each day between origin and destination within date range",
)
async def get_rates(
    date_from: str,
    date_to: str,
    origin: str,
    destination: str,
    db: Database = Depends(database),
) -> Dict[str, Any]:
    """
    Fetch average prices for each day between the origin and destination ports or slug names
    within the specified date range.

    Args:
        date_from (str): The start date in YYYY-MM-DD format.
        date_to (str): The end date in YYYY-MM-DD format.
        origin (str): The origin port code or slug name.
        destination (str): The destination port code or slug name.
        db (Database): The database dependency.

    Returns:
        Dict[str, Any]: A list of average prices for each day or an error response.
    """
    try:
        error_msg = []
        async with db.connect() as conn:
            # Validate if the port or slug name is valid
            port_origin = await get_port_codes(conn, origin)
            port_destination = await get_port_codes(conn, destination)
            # Validate the date range provided
            validate_date = await validate_dates(date_from, date_to)
            if not port_origin:
                error_msg.append(
                    f"Origin port code or slug name provided {origin} is not valid"
                )
            if not port_destination:
                error_msg.append(
                    f"Destination port code or slug name provided {destination} is not valid"
                )
            if validate_date:
                error_msg.append(validate_date)
            if error_msg:
                return response_error(
                    404,
                    "Invalid input data, more information in details",
                    error_msg,
                )

            origin_list = ",".join("'" + row[0] + "'" for row in port_origin)
            destination_list = ",".join("'" + row[0] + "'" for row in port_destination)
            result = await get_average_prices(
                conn, origin_list, destination_list, date_from, date_to
            )
            await conn.close()
        if result:
            return [row._asdict() for row in result]
        return []
    except asyncpg.PostgresError as e:
        LOG.error("Database error: %s", e)
        raise HTTPException(status_code=500, detail=f"Database error: {e}") from e
    except Exception as e:
        LOG.error("Unexpected error: %s", e)
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}") from e
