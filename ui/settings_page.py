from __future__ import annotations
from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QComboBox,QCheckBox,QFormLayout,QFrame
from PySide6.QtCore import Signal
class SettingsPage(QWidget):
    changed=Signal()
    def __init__(self,parent=None):
        super().__init__(parent);l=QVBoxLayout(self);title=QLabel("Settings");title.setObjectName("pageTitle");l.addWidget(title);card=QFrame();card.setObjectName("glassCard");form=QFormLayout(card);self.accent=QComboBox();self.accent.addItems(["Sky Blue","Lavender","Mint","Rose"]);self.temp=QComboBox();self.temp.addItems(["Celsius","Fahrenheit"]);self.wind=QComboBox();self.wind.addItems(["m/s","mph"]);self.pressure=QComboBox();self.pressure.addItems(["hPa","mmHg"]);self.notifications=QCheckBox("Enable desktop weather notifications");self.notifications.setChecked(True)
        for label,w in [("Accent color",self.accent),("Temperature",self.temp),("Wind speed",self.wind),("Pressure",self.pressure),("Notifications",self.notifications)]:form.addRow(label,w);w.currentIndexChanged.connect(self.changed) if hasattr(w,'currentIndexChanged') else w.toggled.connect(self.changed)
        l.addWidget(card);l.addStretch()
