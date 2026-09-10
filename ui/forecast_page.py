from __future__ import annotations
from PySide6.QtWidgets import QWidget,QVBoxLayout,QScrollArea,QWidget as W,QHBoxLayout,QLabel
from components.forecast_card import ForecastCard
from components.chart_card import ChartCard
from utils.units import celsius
class ForecastPage(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent);l=QVBoxLayout(self);title=QLabel("48-hour forecast");title.setObjectName("pageTitle");l.addWidget(title);self.chart=ChartCard("Temperature outlook");l.addWidget(self.chart);scroll=QScrollArea();scroll.setWidgetResizable(True);body=W();self.row=QHBoxLayout(body);scroll.setWidget(body);l.addWidget(scroll);self.days=QVBoxLayout();l.addLayout(self.days)
    def update_forecast(self,data,unit="C"):
        self.chart.update([x['temp'] for x in data]);
        while self.row.count():self.row.takeAt(0).widget().deleteLater()
        while self.days.count():self.days.takeAt(0).widget().deleteLater()
        for x in data[:16]:self.row.addWidget(ForecastCard(x['time'].strftime('%a %H:%M'),x['condition'],celsius(x['temp'],unit),f"{max(0,x['humidity']-20)}%",f"{x['wind']:.1f} m/s"))
        for x in data[::8][:7]:self.days.addWidget(QLabel(f"{x['time'].strftime('%A')}     {x['condition']}     {celsius(x['temp'],unit)}     Humidity {x['humidity']}%",objectName="forecastRow"))
