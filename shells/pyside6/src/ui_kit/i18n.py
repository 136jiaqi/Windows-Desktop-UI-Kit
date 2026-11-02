"""Shell-level language selection and persistence."""

from __future__ import annotations

from PySide6.QtCore import QObject, QLocale, QSettings, Signal
from PySide6.QtWidgets import QLayout, QLineEdit, QPushButton, QLabel, QWidget


class LanguageManager(QObject):
    """Stores a supported UI language once for all shell consumers."""

    changed = Signal(str)
    SUPPORTED = {"zh", "en"}

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.settings = QSettings("WindowsDesktopUIKit", "PySide6Shell")
        saved = self.settings.value("ui_language", "")
        self._language = self._normalize(str(saved)) if saved else self._system_default()

    @staticmethod
    def _normalize(value: str) -> str:
        return "zh" if value.lower().replace("_", "-") in {"zh", "zh-cn", "zh-sg"} else "en"

    def _system_default(self) -> str:
        return "zh" if QLocale.system().name().lower().replace("_", "-") in {"zh-cn", "zh-sg"} else "en"

    @property
    def language(self) -> str:
        return self._language

    def set_language(self, language: str) -> None:
        language = self._normalize(language)
        if language == self._language:
            return
        self._language = language
        self.settings.setValue("ui_language", language)
        self.changed.emit(language)


def apply_text_map(root: QWidget, text_map: dict[str, str]) -> None:
    """Translate existing controls in place, then force Qt to reflow their layouts."""
    for label in root.findChildren(QLabel):
        if label.text() in text_map:
            label.setText(text_map[label.text()])
    for button in root.findChildren(QPushButton):
        if button.text() in text_map:
            button.setText(text_map[button.text()])
    for field in root.findChildren(QLineEdit):
        if field.text() in text_map:
            field.setText(text_map[field.text()])
        if field.placeholderText() in text_map:
            field.setPlaceholderText(text_map[field.placeholderText()])
    _refresh_layout(root.layout())
    root.updateGeometry()
    root.update()


def _refresh_layout(layout: QLayout | None) -> None:
    if layout is None:
        return
    layout.invalidate()
    for index in range(layout.count()):
        item = layout.itemAt(index)
        if item.layout():
            _refresh_layout(item.layout())
        if item.widget():
            layout_attr = getattr(item.widget(), "layout", None)
            child_layout = layout_attr() if callable(layout_attr) else layout_attr
            _refresh_layout(child_layout)
    layout.activate()
