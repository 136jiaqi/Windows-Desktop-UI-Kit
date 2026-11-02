"""Custom title bar used by :class:`ShellWindow`."""

from __future__ import annotations

from PySide6.QtCore import QEvent, Qt, Signal
from PySide6.QtGui import QIcon, QMouseEvent
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget


class TitleBar(QWidget):
    """A presentation-only title bar; window operations are emitted as signals."""

    minimize_requested = Signal()
    maximize_requested = Signal()
    close_requested = Signal()
    language_requested = Signal()
    drag_requested = Signal()
    title_double_clicked = Signal()

    HEIGHT = 44

    def __init__(self, app_name: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("titleBar")
        self.setFixedHeight(self.HEIGHT)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 8, 0)
        layout.setSpacing(8)

        self.icon_label = QLabel()
        self.icon_label.setObjectName("appIcon")
        self.icon_label.setFixedSize(20, 20)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setText("◆")  # Generic placeholder until a product supplies an icon.
        self.name_label = QLabel(app_name)
        self.name_label.setObjectName("appName")

        self.language_button = self._button("简中/EN", "languageButton")
        self.minimize_button = self._button("−", "windowButton")
        self.maximize_button = self._button("□", "windowButton")
        self.close_button = self._button("×", "closeButton")
        for button in (self.language_button, self.minimize_button, self.maximize_button, self.close_button):
            button.setProperty("titleControl", True)

        layout.addWidget(self.icon_label)
        layout.addWidget(self.name_label)
        layout.addStretch(1)
        layout.addWidget(self.language_button)
        layout.addWidget(self.minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(self.close_button)

        self.language_button.clicked.connect(self.language_requested)
        self.minimize_button.clicked.connect(self.minimize_requested)
        self.maximize_button.clicked.connect(self.maximize_requested)
        self.close_button.clicked.connect(self.close_requested)

    def _button(self, text: str, object_name: str) -> QPushButton:
        button = QPushButton(text)
        button.setObjectName(object_name)
        button.setCursor(Qt.CursorShape.ArrowCursor)
        button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        return button

    def set_app_icon(self, icon: QIcon) -> None:
        """Show a supplied app icon, while keeping the title bar independent."""
        self.icon_label.clear()
        self.icon_label.setPixmap(icon.pixmap(18, 18))

    def set_language_label(self, language: str) -> None:
        """Keep a stable bilingual label while ShellWindow tracks the active locale."""
        self.language_button.setText("简中/EN")

    def set_maximized(self, maximized: bool) -> None:
        self.maximize_button.setText("❐" if maximized else "□")

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton and not self.childAt(event.position().toPoint()):
            self.drag_requested.emit()
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton and not self.childAt(event.position().toPoint()):
            self.title_double_clicked.emit()
            event.accept()
            return
        super().mouseDoubleClickEvent(event)
