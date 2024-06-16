"""DB Crud operations lib"""

from typing import List
from sqlalchemy import text
from sqlalchemy.engine import Row
from sqlalchemy.ext.asyncio import AsyncConnection

# SQL query template for fetching average prices
QUERY = """ SELECT day,
            CASE 
               WHEN COUNT(price) >= 3 THEN AVG(price) 
               ELSE NULL 
            END AS average_price 
            FROM prices
            WHERE orig_code in ({}) and
                  dest_code in ({}) and 
                  day between '{}' and '{}'
            GROUP BY day
            ORDER BY day"""


async def get_average_prices(
    c: AsyncConnection,
    origin: str,
    destination: str,
    date_from: str,
    date_to: str,
) -> List[Row]:
    """
    Fetches the average prices for the given origin and destination ports
    within the specified date range.

    Parameters:
    c (AsyncConnection): The database connection
    origin (str): Origin port code or region slug
    destination (str): Destination port code or region slug
    date_from (str): Start date for the range (inclusive)
    date_to (str): End date for the range (inclusive)

    Returns:
    List[Row]: A list of rows containing the day and average price,
    with NULL for days having less than 3 prices
    """
    result = await c.execute(
        text(QUERY.format(origin, destination, date_from, date_to))
    )
    return result.fetchall()


async def get_port_codes(c: AsyncConnection, port: str) -> List[Row]:
    """
    Validates the port code or slug name by fetching the corresponding port codes from the database.

    Parameters:
    c (AsyncConnection): The database connection
    port (str): The port code or region slug to validate

    Returns:
    List[Row]: A list of rows containing the port codes
    """
    result = await c.execute(
        text(
            f"select DISTINCT code from ports where code='{port}' or \
            parent_slug in (select slug from regions where slug='{port}' or parent_slug='{port}')"
        )
    )
    return result.fetchall()
