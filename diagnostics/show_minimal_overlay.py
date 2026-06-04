"""
Show a minimal overlay window for manual PyQt/always-on-top checks.
"""

import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QWidget


class SimpleOverlay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("游戏翻译测试")
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint
            | Qt.FramelessWindowHint
            | Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(100, 100, 400, 150)

        self.label = QLabel(
            "游戏语音翻译器\n\n"
            "测试翻译:\n"
            "- Hello team -> 队友\n"
            "- He's one shot -> 他大残了",
            self,
        )
        self.label.setWordWrap(True)
        self.label.setStyleSheet(
            """
            QLabel {
                color: #00FF00;
                font-size: 16px;
                font-family: Microsoft YaHei;
                background: rgba(0,0,0,0.7);
                padding: 10px;
                border: 2px solid #00FF00;
                border-radius: 10px;
            }
            """
        )
        self.label.setGeometry(0, 0, 400, 150)


def main() -> int:
    app = QApplication(sys.argv)
    overlay = SimpleOverlay()
    overlay.show()
    print("Minimal overlay is visible. Close the window to exit.")
    return app.exec_()


if __name__ == "__main__":
    raise SystemExit(main())
