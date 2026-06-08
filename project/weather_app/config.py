"""
Configuration file for the Weather Forecast Application.
Place your OpenWeatherMap API key here.
"""

# OpenWeatherMap API Configuration
API_KEY = "a210674ef68d02049e23979d33e42c33"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Application Settings
DEFAULT_UNITS = "metric"  # metric for Celsius, imperial for Fahrenheit
HISTORY_FILE = "history.json"
MAX_HISTORY_ITEMS = 5
