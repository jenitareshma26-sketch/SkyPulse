"""
Weather API Module - Handles all OpenWeatherMap API interactions.
Separates API logic from GUI logic for better maintainability.
"""

import requests
from typing import Optional, Dict, Any
from io import BytesIO
from PIL import Image
import config


class WeatherAPI:
    """
    Handles communication with the OpenWeatherMap API.
    Provides methods to fetch weather data and weather icons.
    """

    def __init__(self, api_key: str = None):
        """
        Initialize the WeatherAPI with an API key.

        Args:
            api_key: OpenWeatherMap API key. Uses config.API_KEY if not provided.
        """
        self.api_key = api_key or config.API_KEY
        self.base_url = config.BASE_URL

    def get_weather(self, city: str, units: str = "metric") -> Dict[str, Any]:
        """
        Fetch current weather data for a given city.

        Args:
            city: Name of the city to get weather for.
            units: Temperature units - 'metric' for Celsius, 'imperial' for Fahrenheit.

        Returns:
            Dictionary containing weather data or error information.
        """
        if not city or not city.strip():
            return {"success": False, "error": "Please enter a city name."}

        if self.api_key == "YOUR_API_KEY":
            return {"success": False, "error": "Please configure your API key in config.py."}

        params = {
            "q": city.strip(),
            "appid": self.api_key,
            "units": units
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                return self._parse_weather_data(data, units)
            elif response.status_code == 404:
                return {"success": False, "error": f"City '{city}' not found. Please check the spelling."}
            elif response.status_code == 401:
                return {"success": False, "error": "Invalid API key. Please check your configuration."}
            elif response.status_code == 429:
                return {"success": False, "error": "API rate limit exceeded. Please try again later."}
            else:
                return {"success": False, "error": f"API error: {response.status_code}"}

        except requests.exceptions.ConnectionError:
            return {"success": False, "error": "No internet connection. Please check your network."}
        except requests.exceptions.Timeout:
            return {"success": False, "error": "Request timed out. Please try again."}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"Network error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}

    def _parse_weather_data(self, data: Dict[str, Any], units: str) -> Dict[str, Any]:
        """
        Parse raw API response into a structured format.

        Args:
            data: Raw JSON response from OpenWeatherMap API.
            units: Temperature units used in the request.

        Returns:
            Structured dictionary with weather information.
        """
        weather_info = data["weather"][0]
        main_info = data["main"]
        wind_info = data["wind"]

        unit_symbol = "°C" if units == "metric" else "°F"
        speed_unit = "m/s" if units == "metric" else "mph"

        return {
            "success": True,
            "city": data["name"],
            "country": data["sys"].get("country", ""),
            "temperature": f"{round(main_info['temp'])}{unit_symbol}",
            "feels_like": f"{round(main_info['feels_like'])}{unit_symbol}",
            "condition": weather_info["description"].title(),
            "humidity": f"{main_info['humidity']}%",
            "wind_speed": f"{wind_info['speed']} {speed_unit}",
            "icon_code": weather_info["icon"],
            "raw_temp": main_info["temp"],
            "units": units
        }

    def get_weather_icon(self, icon_code: str, size: tuple = (100, 100)) -> Optional[Image.Image]:
        """
        Fetch and return the weather icon from OpenWeatherMap.

        Args:
            icon_code: Icon code from weather data (e.g., '01d', '02n').
            size: Tuple of (width, height) to resize the icon.

        Returns:
            PIL Image object or None if fetch fails.
        """
        icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"

        try:
            response = requests.get(icon_url, timeout=10)
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                image = image.resize(size, Image.Resampling.LANCZOS)
                return image
        except Exception:
            pass

        return None
