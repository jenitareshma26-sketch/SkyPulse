from __future__ import annotations
from PySide6.QtWidgets import QWidget,QHBoxLayout,QLabel,QToolButton
from PySide6.QtCore import QTimer,Signal
from datetime import datetime
class Navbar(QWidget):
    location_requested=Signal(); settings_requested=Signal()
    def __init__(self,parent=None):
        super().__init__(parent); l=QHBoxLayout(self); self.clock=QLabel(); self.clock.setObjectName("muted"); l.addWidget(self.clock);l.addStretch()
        for text,signal in [("⌖",self.location_requested),("⚙",self.settings_requested)]:
            b=QToolButton();b.setText(text);b.setToolTip({"⌖":"Use default location","⚙":"Settings"}[text]);b.clicked.connect(signal);l.addWidget(b)
        self.unit=QToolButton();self.unit.setText("°C");l.addWidget(self.unit); timer=QTimer(self);timer.timeout.connect(self.tick);timer.start(1000);self.tick()
    def tick(self): self.clock.setText(datetime.now().strftime("%A, %d %B  ·  %H:%M:%S"))
