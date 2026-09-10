from __future__ import annotations
def celsius(value: float, unit: str) -> str:
    return f"{value * 9 / 5 + 32:.0f}°F" if unit == "F" else f"{value:.0f}°C"
def wind(value: float, unit: str) -> str:
    return f"{value * 2.23694:.1f} mph" if unit == "mph" else f"{value:.1f} m/s"
def pressure(value: float, unit: str) -> str:
    return f"{value * 0.750062:.0f} mmHg" if unit == "mmHg" else f"{value:.0f} hPa"

