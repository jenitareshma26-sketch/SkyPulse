from __future__ import annotations
from PySide6.QtWidgets import QPushButton
class AnimatedButton(QPushButton):
    def __init__(self,text="",primary=False,parent=None):
        super().__init__(text,parent); self.setCursor(__import__('PySide6').QtCore.Qt.PointingHandCursor); self.setProperty("primary",primary)

