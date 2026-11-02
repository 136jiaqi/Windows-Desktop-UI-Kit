"""Minimal executable proof that business content can be injected into ShellWindow."""

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ui_kit import ShellWindow  # noqa: E402
from ui_kit import require_xmodhub  # noqa: E402


def make_content() -> QWidget:
    content = QWidget()
    content.setObjectName("demoContent")
    layout = QVBoxLayout(content)
    layout.setContentsMargins(28, 24, 28, 28)
    title = QLabel("Windows Desktop UI Kit")
    title.setStyleSheet("color: #F3F4F6; font-size: 22px; font-weight: 600;")
    detail = QLabel("第一阶段：可复用窗口外壳与自定义标题栏")
    detail.setStyleSheet("color: #9CA3AF; font-size: 13px;")
    layout.addWidget(title)
    layout.addWidget(detail)
    layout.addStretch(1)
    return content


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Windows Desktop UI Kit")
    if not require_xmodhub():
        raise SystemExit(0)
    window = ShellWindow("Windows Desktop UI Kit")
    window.set_content(make_content())
    window.resize(980, 640)
    window.show()
    raise SystemExit(app.exec())
