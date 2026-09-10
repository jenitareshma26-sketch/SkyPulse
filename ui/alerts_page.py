from __future__ import annotations
from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QFrame
class AlertsPage(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent);self.l=QVBoxLayout(self);title=QLabel("Weather alerts");title.setObjectName("pageTitle");self.l.addWidget(title);self.content=QVBoxLayout();self.l.addLayout(self.content);self.l.addStretch()
    def update_alerts(self,alerts):
        while self.content.count():self.content.takeAt(0).widget().deleteLater()
        for title,message in alerts:
            card=QFrame();card.setObjectName("card");l=QVBoxLayout(card);h=QLabel(title);h.setObjectName("sectionTitle");l.addWidget(h);l.addWidget(QLabel(message));self.content.addWidget(card)

