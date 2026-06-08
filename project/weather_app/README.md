# Weather Forecast App

A modern, user-friendly desktop weather application built with Python and Tkinter. This applicationfetches real-time weather data from the OpenWeatherMap API and displays it in a clean, intuitive interface.

## Features

- **Current Weather Display**: View real-time weather data including:
  - City name and country
  - Current temperature
  - Weather condition with description
  -Humidity percentage
  - Wind speed
  - Feels like temperature
  - Weather icon

- **Unit Selection**: Switch between Celsius and Fahrenheit with a simple dropdown

- **Search History**: Automatically saves your last 5 searched cities for quick access

- **Modern GUI**: Clean, light-themed interface with intuitive controls

- **Error Handling**: Robust error handling for:
  - Invalid city names
  - No internet connection
  - API errors
  - Empty input fields

- **Date & Time Display**: Shows current date and time with automatic updates

- **Refresh Button**: Quickly update weather data for the current city

## Project Structure

```
weather_app/
├── main.py          # Main application with GUI
├── weather_api.py   # API interaction module
├── config.py        # Configuration file (API key)
├── history.json     # Search history storage
├── requirements.txt # Python dependencies
└── README.md        # This file
```

## Prerequisites

- Python 3.7 or higher
- OpenWeatherMap API key (free tier available)

## Getting an OpenWeatherMap API Key

1. Go to [OpenWeatherMap](https://openweathermap.org/)
2. Click "Sign Up" in the top-right corner
3. Fill in your details and create an account
4. After logging in, go to "My API Keys" in your account dashboard
5. Your default API key will be displayed, or you can create a new one
6. Free tier allows 1,000 API calls per day

## Installation

1. **Clone or download this repository**

2. **Navigate to the project directory**:
   ```bash
   cd weather_app
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your API key**:
   
   Open `config.py` in a text editor and replace `YOUR_API_KEY` with your actual OpenWeatherMap API key:
   ```python
   API_KEY = "your_actual_api_key_here"
   ```

## Running the Application

1. Navigate to the project directory:
   ```bash
   cd weather_app
   ```

2. Run the application:
   ```bash
   python main.py
   ```

## Usage

1. Enter a city name in the search field
2. Select your preferred temperature unit (Celsius or Fahrenheit)
3. Click "Get Weather" to fetch current weather data
4. Use the dropdown to access previously searched cities
5. Click the refresh button to update weather data

## Technical Details

- **GUI Framework**: Tkinter (Python standard library)
- **API**: OpenWeatherMap REST API
- **Image Processing**: Pillow (PIL) for weather icons
- **HTTP Requests**: requests library
- **Data Storage**: JSON file for search history

## Error Handling

The application handles various error scenarios:
- **404 City Not Found**: Displays user-friendly message for invalid city names
- **401 Unauthorized**: Alerts user to check API key configuration
- **429 Rate Limited**: Informs user when API quota is exceeded
- **Connection Errors**: Detects and reports network connectivity issues
- **Timeout Errors**: Handles slow or unresponsive API requests

## License

This project is open source and available for personal and educational use.

## Contributing

Feel free to submit issues and pull requests for improvements or bug fixes.

## Acknowledgments

- Weather data provided by [OpenWeatherMap](https://openweathermap.org/)
- Icons from OpenWeatherMap's weather icon set
