from __future__ import annotations
from PySide6.QtWidgets import QFrame,QVBoxLayout,QLabel,QHBoxLayout
from PySide6.QtCore import Qt
class WeatherCard(QFrame):
    def __init__(self,title,value,detail="",symbol="✦",parent=None):
        super().__init__(parent); self.setObjectName("metricCard"); box=QVBoxLayout(self); box.setContentsMargins(18,16,18,16); head=QHBoxLayout(); self.symbol=QLabel(symbol);self.symbol.setObjectName("metricSymbol");self.title=QLabel(title);self.title.setObjectName("muted");head.addWidget(self.symbol);head.addWidget(self.title);head.addStretch();self.value=QLabel(value);self.value.setObjectName("metric");self.detail=QLabel(detail);self.detail.setObjectName("muted");box.addLayout(head);box.addWidget(self.value);box.addWidget(self.detail)
    def update_value(self,value,detail=""):
        self.value.setText(value); self.detail.setText(detail)
