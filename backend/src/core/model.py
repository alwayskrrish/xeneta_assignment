"""Pydantic BaseModel for FastAPI"""

from typing import Optional
from datetime import date
from pydantic import BaseModel


class PriceResponse(BaseModel):
    """
    BaseModel structure for the get prices response API.
    This model defines the schema for the response object that
    will be returned by the API when querying average prices.

    Attributes:
    - day (date): The date for which the average price is calculated.
    - average_price (Optional[float]): The average price for the given day.
      This field is optional and can be None if there are less than 3 prices.
    """

    day: date
    average_price: Optional[float]
