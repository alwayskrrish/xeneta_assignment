"""Library utilities for FastAPI"""

from typing import List, Optional
from fastapi.responses import JSONResponse


def response_error(
    status_code: int, message: str, details: Optional[List[str]] = None
) -> JSONResponse:
    """
    Create a JSON response for errors in FastAPI.

    This utility function helps to standardize error responses throughout the API.
    It generates a JSON response with a given status code, error message, and optional details.

    Args:
        status_code (int): The HTTP status code for the error response.
        message (str): A brief message describing the error.
        details (Optional[List[str]]): Additional details about the error, if any.

    Returns:
        JSONResponse: A JSON response containing the status code, message, and details.
    """
    return JSONResponse(
        status_code=status_code,
        content={
            "status_code": status_code,
            "message": message,
            "details": details or [],
        },
    )
