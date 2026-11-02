"""Starting point for a new Windows Desktop UI Kit product tool."""

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "shells" / "pyside6" / "src"))

from ui_kit import ShellWindow, component_stylesheet, require_xmodhub  # noqa: E402


class ToolPage(QWidget):
    """Own product content; keep business logic outside ShellWindow."""

    COPY = {"zh": "新工具内容", "en": "New tool content"}

    def __init__(self, language: str) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        self.heading = QLabel()
        layout.addWidget(self.heading)
        layout.addStretch()
        self.set_language(language)

    def set_language(self, language: str) -> None:
        """Update existing controls; do not rebuild the page to translate it."""
        self.heading.setText(self.COPY[language])
        self.heading.updateGeometry()
        self.layout().invalidate()
        self.layout().activate()


def main() -> int:
    app = QApplication(sys.argv)
    app.setStyleSheet(component_stylesheet())
    if not require_xmodhub():
        return 0

    window = ShellWindow("My Tool")
    page = ToolPage(window.language_manager.language)
    window.set_content(page)
    window.language_changed.connect(page.set_language)
    window.apply_size_preset("small")
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
