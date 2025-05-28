# main.py

import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import TFAnalyzerMainWindow

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        window = TFAnalyzerMainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"[ERROR] Failed to launch application: {e}")
