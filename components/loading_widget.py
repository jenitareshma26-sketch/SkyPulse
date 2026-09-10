from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt
class LoadingWidget(QLabel):
    def __init__(self,parent=None): super().__init__("Updating weather intelligence…",parent);self.setAlignment(Qt.AlignCenter)

