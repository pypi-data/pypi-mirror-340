"""
simple_weather - A beginner-friendly Python package for fetching weather data.

This package provides simple functions to fetch weather data and moon phases
from weather services, with built-in caching and error handling to make it suitable
for educational use.
"""

__version__ = "0.1.0"

from .core import clear_cache, get_weather, set_cache_duration, set_user_agent

# For convenience, provide the most commonly used functions at the top level
__all__ = ["get_weather", "clear_cache", "set_cache_duration", "set_user_agent"]
