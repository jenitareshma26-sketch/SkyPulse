from __future__ import annotations
from PySide6.QtWidgets import QFrame,QVBoxLayout,QLabel,QPushButton
from PySide6.QtCore import Signal
class Sidebar(QFrame):
    page_requested=Signal(str)
    def __init__(self,parent=None):
        super().__init__(parent); self.setObjectName("sidebar"); l=QVBoxLayout(self);l.setContentsMargins(12,22,12,20); logo=QLabel("☁  SkyPulse\n     Pro"); logo.setObjectName("logo"); l.addWidget(logo); tagline=QLabel("WEATHER, ELEVATED");tagline.setObjectName("brandTag");l.addWidget(tagline);l.addSpacing(22);self.buttons={}
        for key,text in [("dashboard","⌂   Overview"),("forecast","◷   Forecast"),("map","⌖   Weather map"),("alerts","⚠   Alerts"),("settings","⚙   Settings")]:
            b=QPushButton(text);b.setObjectName("nav");b.clicked.connect(lambda _,x=key:self.page_requested.emit(x));l.addWidget(b);self.buttons[key]=b
        l.addStretch(); credit=QLabel("Made with ♥ by\nJENITA RESHMA P\n\nSkyPulse Pro  ·  Version 2.0");credit.setObjectName("brandCredit");l.addWidget(credit)
