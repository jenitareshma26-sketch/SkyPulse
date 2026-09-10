from __future__ import annotations
from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Signal
class SearchBar(QLineEdit):
    submitted=Signal(str)
    def __init__(self,parent=None):
        super().__init__(parent); self.setPlaceholderText("Search a city, country, or coordinates…"); self.setClearButtonEnabled(True); self.returnPressed.connect(lambda:self.submitted.emit(self.text().strip()))

