"""Generic logging configuration for different components"""

from typing import Any, Dict

# Logging configuration dictionary
LOG_CONFIG = {
    "version": 1,
    "formatters": {
        "default": {
            "class": "logging.Formatter",
            "format": "%(asctime)s.%(msecs)03d %(levelname)s %(name)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "uvicorn": {
            "class": "logging.Formatter",
            "format": "%(asctime)s.%(msecs)03d %(levelname)s uvicorn: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "default": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stderr",
        },
        "uvicorn": {
            "class": "logging.StreamHandler",
            "formatter": "uvicorn",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {
        "uvicorn": {
            "handlers": ["uvicorn"],
            "level": "INFO",
            "propagate": False,
        },
        "default": {
            "handlers": ["default"],
            "level": "DEBUG",
        },
        "rate_calculator": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": True,
        },
    },
}


def get_config(*, log_level: str = "DEBUG") -> Dict[str, Any]:
    """
    Returns a logging configuration with the specified log level.
    """
    cfg = {**LOG_CONFIG}
    cfg["loggers"]["default"]["level"] = log_level
    cfg["loggers"]["rate_calculator"]["level"] = log_level
    return cfg
