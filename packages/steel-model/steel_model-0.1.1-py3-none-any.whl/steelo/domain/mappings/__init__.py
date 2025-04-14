"""
This package contains mapping data for various domain concepts.

It provides dictionaries and utility functions for accessing reference data
that is used throughout the application.
"""

from .country import (
    COUNTRY_TO_CODE_MAP,
    COUNTRY_TO_IRENA_MAP,
    COUNTRY_TO_REGION_MAP,
    COUNTRY_TO_SSP_REGION_MAP,
    GEM_COUNTRY_WS_REGION_MAP,
)

__all__ = [
    "COUNTRY_TO_CODE_MAP",
    "COUNTRY_TO_IRENA_MAP",
    "COUNTRY_TO_REGION_MAP",
    "COUNTRY_TO_SSP_REGION_MAP",
    "GEM_COUNTRY_WS_REGION_MAP",
]
