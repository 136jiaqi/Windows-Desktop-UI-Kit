"""Product-neutral reusable controls for the PySide6 shell."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (QCheckBox, QDialog, QDialogButtonBox, QFrame,
                               QHBoxLayout, QLabel, QLineEdit, QPushButton,
                               QProgressBar, QScrollArea, QSizePolicy, QVBoxLayout, QWidget)

from .tokens import COLORS, SPACING


class PrimaryButton(QPushButton):
    def __init__(self, text: str, parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.setObjectName("primaryButton")


class SecondaryButton(QPushButton):
    def __init__(self, text: str, parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.setObjectName("secondaryButton")


class IconButton(QPushButton):
    def __init__(self, icon_text: str, tooltip: str = "", parent: QWidget | None = None) -> None:
        super().__init__(icon_text, parent)
        self.setObjectName("iconButton")
        self.setToolTip(tooltip)


class Card(QFrame):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("card")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(SPACING["lg"], SPACING["lg"], SPACING["lg"], SPACING["lg"])
        self.layout.setSpacing(SPACING["md"])


class StatusBadge(QLabel):
    _colors = {"success": COLORS["success"], "warning": COLORS["warning"], "danger": COLORS["danger"], "neutral": "#536177"}
    def __init__(self, text: str, tone: str = "neutral", parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.set_tone(tone)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedHeight(22)
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        self.setMaximumWidth(112)

    def set_tone(self, tone: str) -> None:
        color = self._colors.get(tone, self._colors["neutral"])
        self.setStyleSheet(f"background: {color}; color: white; border-radius: 11px; padding: 0 8px; font-size: 11px; font-weight: 600;")


class ToggleSwitch(QCheckBox):
    def __init__(self, checked: bool = False, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("toggle")
        self.setChecked(checked)
        self.setCursor(Qt.CursorShape.PointingHandCursor)


class ProgressBar(QProgressBar):
    def __init__(self, value: int = 0, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setRange(0, 100)
        self.setValue(value)
        self.setTextVisible(False)


class ScrollArea(QScrollArea):
    def __init__(self, widget: QWidget | None = None, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("scrollArea")
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        if widget:
            self.setWidget(widget)


class FormInput(QLineEdit):
    def __init__(self, placeholder: str = "", value: str = "", parent: QWidget | None = None) -> None:
        super().__init__(value, parent)
        self.setObjectName("formInput")
        self.setPlaceholderText(placeholder)


class SectionHeader(QWidget):
    def __init__(self, title: str, subtitle: str = "", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(3)
        self.title = QLabel(title); self.title.setObjectName("sectionTitle")
        self.subtitle = QLabel(subtitle); self.subtitle.setObjectName("sectionSubtitle"); self.subtitle.setWordWrap(True)
        layout.addWidget(self.title); layout.addWidget(self.subtitle)


class SidebarNavigation(QFrame):
    changed = Signal(str)
    def __init__(self, items: list[tuple[str, str]], parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setFixedWidth(220)
        self.setStyleSheet(f"QFrame#sidebar {{ background: {COLORS['surface']}; border-right: 1px solid {COLORS['border']}; }}")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 16, 12, 16)
        layout.setSpacing(6)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.buttons: dict[str, QPushButton] = {}
        for key, label in items:
            button = QPushButton(label); button.setObjectName("sidebarItem"); button.setCheckable(True)
            button.clicked.connect(lambda checked=False, value=key: self.select(value))
            self.buttons[key] = button; layout.addWidget(button)
        if items: self.select(items[0][0])

    def select(self, key: str) -> None:
        for name, button in self.buttons.items():
            button.setChecked(name == key)
        self.changed.emit(key)


class Dialog(QDialog):
    def __init__(self, title: str, body: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumWidth(380)
        self.setModal(True)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(14)
        heading = QLabel(title); heading.setObjectName("sectionTitle")
        body_label = QLabel(body); body_label.setWordWrap(True); body_label.setObjectName("mutedText")
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(heading); layout.addWidget(body_label); layout.addWidget(buttons)
