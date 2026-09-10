# SkyPulse Pro

A polished PySide6 desktop weather workstation with live OpenWeather support, OpenStreetMap/Nominatim discovery, a responsive offline mode, forecasts, air quality, alerts, preferences, SQLite search history, and dark/light themes.

## Run

```bash
python -m venv .venv
. .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env  # optional: add OPENWEATHER_API_KEY for live observations
python main.py
```

Without an API key the application intentionally remains usable using local deterministic weather estimates. Searches still use Nominatim when online; coordinates always work.
