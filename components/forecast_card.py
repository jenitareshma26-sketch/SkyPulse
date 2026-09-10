from __future__ import annotations
from PySide6.QtWidgets import QFrame,QVBoxLayout,QLabel
from components.weather_icon import WeatherIcon
from PySide6.QtCore import Qt
class ForecastCard(QFrame):
    def __init__(self,when,condition,temp,rain="—",wind="—",parent=None):
        super().__init__(parent);self.setObjectName("forecastCard");l=QVBoxLayout(self);l.setContentsMargins(12,14,12,14);time=QLabel(when);time.setObjectName("forecastTime");l.addWidget(time,alignment=Qt.AlignCenter);l.addWidget(WeatherIcon(condition,58),alignment=Qt.AlignCenter);degree=QLabel(temp);degree.setObjectName("forecastTemp");l.addWidget(degree,alignment=Qt.AlignCenter);meta=QLabel(f"☂ {rain}\n↗ {wind}");meta.setObjectName("forecastMeta");meta.setAlignment(Qt.AlignCenter);l.addWidget(meta)
