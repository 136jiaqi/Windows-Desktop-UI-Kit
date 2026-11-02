"""Reusable frameless Windows shell with native Qt system move/resize hooks."""

from __future__ import annotations

from PySide6.QtCore import QEvent, QPoint, Qt, Signal
from PySide6.QtGui import QIcon, QMouseEvent, QResizeEvent
from PySide6.QtWidgets import QFrame, QGraphicsDropShadowEffect, QVBoxLayout, QWidget

from .title_bar import TitleBar
from .tokens import component_stylesheet
from .i18n import LanguageManager


class ShellWindow(QWidget):
    """A product-neutral shell which accepts arbitrary content below its title bar.

    `set_content()` is the only API a product screen needs to use.  Window handling
    remains here, rather than leaking into game/tool UI code.
    """

    RESIZE_MARGIN = 8
    SMALL_TOOL_SIZE = (900, 620)
    LARGE_TOOL_SIZE = (1180, 760)
    language_changed = Signal(str)

    def __init__(self, app_name: str = "Desktop Tool", app_icon: QIcon | None = None, language: str | None = None) -> None:
        super().__init__()
        self.setWindowTitle(app_name)
        if app_icon:
            self.setWindowIcon(app_icon)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self.setMinimumSize(760, 520)

        self._root = QFrame(self)
        self._root.setObjectName("shellRoot")
        self._root.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(24)
        shadow.setOffset(0, 6)
        shadow.setColor("#66000000")
        self._root.setGraphicsEffect(shadow)

        self._layout = QVBoxLayout(self._root)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self.language_manager = LanguageManager(self)
        if language is not None:
            self.language_manager.set_language(language)
        self.title_bar = TitleBar(app_name)
        self.title_bar.set_language_label(self.language_manager.language)
        if app_icon:
            self.title_bar.set_app_icon(app_icon)
        self._layout.addWidget(self.title_bar)
        self._content: QWidget | None = None

        self.title_bar.minimize_requested.connect(self.showMinimized)
        self.title_bar.maximize_requested.connect(self.toggle_maximized)
        self.title_bar.close_requested.connect(self.close)
        self.title_bar.language_requested.connect(self.toggle_language)
        self.language_manager.changed.connect(self._on_language_changed)
        self.title_bar.drag_requested.connect(self._start_system_move)
        self.title_bar.title_double_clicked.connect(self.toggle_maximized)
        self.installEventFilter(self)
        self._apply_style()

    def _on_language_changed(self, language: str) -> None:
        self.title_bar.set_language_label(language)
        self.language_changed.emit(language)

    def set_language_label(self, language: str) -> None:
        self.set_language(language)

    def set_language(self, language: str) -> None:
        self.language_manager.set_language(language)

    def toggle_language(self) -> None:
        self.set_language("en" if self.language_manager.language == "zh" else "zh")

    def set_content(self, content: QWidget) -> None:
        """Insert and own the product-specific content widget."""
        if self._content is not None:
            self._layout.removeWidget(self._content)
            self._content.deleteLater()
        self._content = content
        self._content.setParent(self._root)
        self._layout.addWidget(content, 1)

    def apply_size_preset(self, preset: str) -> None:
        """Apply a documented starter size: ``small`` or ``large``."""
        width, height = self.SMALL_TOOL_SIZE if preset == "small" else self.LARGE_TOOL_SIZE
        self.resize(width, height)

    def toggle_maximized(self) -> None:
        self.showNormal() if self.isMaximized() else self.showMaximized()

    def changeEvent(self, event: QEvent) -> None:
        if event.type() == QEvent.Type.WindowStateChange:
            self.title_bar.set_maximized(self.isMaximized())
            self._update_geometry()
        super().changeEvent(event)

    def resizeEvent(self, event: QResizeEvent) -> None:
        self._update_geometry()
        super().resizeEvent(event)

    def _update_geometry(self) -> None:
        # Keep a transparent perimeter for the shadow only in normal state.
        margin = 0 if self.isMaximized() else 12
        self._root.setGeometry(self.rect().adjusted(margin, margin, -margin, -margin))

    def _start_system_move(self) -> None:
        handle = self.windowHandle()
        if handle and not self.isMaximized():
            handle.startSystemMove()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton and not self.isMaximized():
            edge = self._resize_edge(event.position().toPoint())
            handle = self.windowHandle()
            if edge != Qt.Edge(0) and handle:
                handle.startSystemResize(edge)
                event.accept()
                return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if not self.isMaximized():
            edge = self._resize_edge(event.position().toPoint())
            self.setCursor(self._cursor_for_edge(edge))
        else:
            self.unsetCursor()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        self.unsetCursor()
        super().leaveEvent(event)

    def _resize_edge(self, point: QPoint) -> Qt.Edge:
        m, w, h = self.RESIZE_MARGIN, self.width(), self.height()
        edge = Qt.Edge(0)
        if point.x() <= m:
            edge |= Qt.Edge.LeftEdge
        elif point.x() >= w - m:
            edge |= Qt.Edge.RightEdge
        if point.y() <= m:
            edge |= Qt.Edge.TopEdge
        elif point.y() >= h - m:
            edge |= Qt.Edge.BottomEdge
        return edge

    @staticmethod
    def _cursor_for_edge(edge: Qt.Edge) -> Qt.CursorShape:
        if edge in (Qt.Edge.LeftEdge, Qt.Edge.RightEdge):
            return Qt.CursorShape.SizeHorCursor
        if edge in (Qt.Edge.TopEdge, Qt.Edge.BottomEdge):
            return Qt.CursorShape.SizeVerCursor
        if edge in (Qt.Edge.TopEdge | Qt.Edge.LeftEdge, Qt.Edge.BottomEdge | Qt.Edge.RightEdge):
            return Qt.CursorShape.SizeFDiagCursor
        if edge:
            return Qt.CursorShape.SizeBDiagCursor
        return Qt.CursorShape.ArrowCursor

    def _apply_style(self) -> None:
        self.setStyleSheet(component_stylesheet() + """
            QFrame#shellRoot { background: #0B0F17; border: 1px solid #293241; border-radius: 12px; }
            QWidget#titleBar { background: #0B0F17; border-top-left-radius: 12px; border-top-right-radius: 12px; }
            QLabel#appIcon { background: #3730A3; border-radius: 5px; color: #F3F4F6; }
            QLabel#appName { color: #F3F4F6; font-size: 13px; font-weight: 600; }
            QPushButton { border: 0; background: transparent; color: #9CA3AF; font-size: 12px; }
            QPushButton#languageButton { min-width: 68px; padding: 0 8px; border-radius: 5px; }
            QPushButton#windowButton, QPushButton#closeButton { min-width: 32px; max-width: 32px; min-height: 28px; font-size: 17px; border-radius: 5px; }
            QPushButton:hover { background: #151B26; color: #F3F4F6; }
            QPushButton#closeButton:hover { background: #C2410C; color: #FFFFFF; }
            QPushButton:disabled { color: #596273; background: transparent; }
        """)
