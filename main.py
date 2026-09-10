"""SkyPulse Pro application entry point."""
from __future__ import annotations
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from ui.splash_screen import SplashScreen
from ui.main_window import MainWindow
def main() -> int:
    app=QApplication(sys.argv);app.setApplicationName("SkyPulse Pro");app.setStyle("Fusion");splash=SplashScreen();splash.show();window=MainWindow();QTimer.singleShot(850,lambda:(window.showMaximized(),splash.finish(window)));return app.exec()
if __name__ == "__main__":raise SystemExit(main())
