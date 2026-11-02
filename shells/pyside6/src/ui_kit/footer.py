"""Reusable third-party disclosure footer with an interactive popover."""
from __future__ import annotations
from dataclasses import dataclass
from html import escape
from PySide6.QtCore import QEvent, QObject, QPoint, QTimer, QUrl, Qt
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QVBoxLayout, QWidget

@dataclass(frozen=True)
class ThirdPartyFooterConfig:
    provider_name: str = "Bufftool"
    provider_url: str = "https://www.bufftool.com/"
    disclaimer_zh: str = "1. 本工具由三方[Bufftool]提供并负责\n2. 工具设计遵循合规性原则，不干扰游戏正常运行、不破坏游戏平衡，亦不算改游戏核心程序、数据或相关配置文件，仅提供合规辅助功能，严禁用于任何违法用途\n3. 使用本工具视为已充分了解并接受本工具所有潜在风险，如因异常使用导致的任何问题由玩家自行承担"
    disclaimer_en: str = "1. This tool is provided and maintained by the third party [Bufftool].\n2. Its design follows compliance principles: it does not interfere with normal game operation or game balance, and does not alter core game programs, data, or related configuration files. It provides only compliant auxiliary features and must not be used for any unlawful purpose.\n3. By using this tool, you confirm that you understand and accept all potential risks. Any issues caused by abnormal use are the player's own responsibility."
    visible: bool = True

class DisclosurePopover(QFrame):
    def __init__(self, config: ThirdPartyFooterConfig, parent: QWidget) -> None:
        super().__init__(None, Qt.WindowType.Tool | Qt.WindowType.FramelessWindowHint)
        self.config, self.owner = config, parent; self.setObjectName("disclosurePopover")
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating); self.setFixedWidth(400)
        layout = QVBoxLayout(self); layout.setContentsMargins(14, 12, 14, 12)
        self.text = QLabel(); self.text.setWordWrap(True); self.text.setTextFormat(Qt.TextFormat.RichText); self.text.setOpenExternalLinks(False)
        self.text.linkActivated.connect(lambda url: QDesktopServices.openUrl(QUrl(url))); layout.addWidget(self.text)
        self.hide_timer = QTimer(self); self.hide_timer.setSingleShot(True); self.hide_timer.timeout.connect(self.hide)

    def set_language(self, language: str) -> None:
        raw = self.config.disclaimer_zh if language == "zh" else self.config.disclaimer_en
        safe = escape(raw).replace("[Bufftool]", f'<a href="{self.config.provider_url}">Bufftool</a>').replace("\n", "<br><br>")
        self.text.setText(safe); self.adjustSize(); self.setFixedHeight(min(max(self.sizeHint().height(), 150), 340))

    def show_for(self, anchor: QWidget) -> None:
        self.hide_timer.stop(); self.set_language(getattr(anchor.parent(), "language", "zh"))
        pos = anchor.mapToGlobal(QPoint(anchor.width() - self.width(), -self.height() - 8))
        screen = anchor.screen().availableGeometry()
        if pos.y() < screen.top(): pos.setY(anchor.mapToGlobal(QPoint(0, anchor.height() + 8)).y())
        pos.setX(max(screen.left() + 8, min(pos.x(), screen.right() - self.width() - 8))); self.move(pos); self.show(); self.raise_()

    def enterEvent(self, event: QEvent) -> None: self.hide_timer.stop(); super().enterEvent(event)
    def leaveEvent(self, event: QEvent) -> None: self.hide_timer.start(180); super().leaveEvent(event)

class ThirdPartyFooter(QWidget):
    def __init__(self, config: ThirdPartyFooterConfig | None = None, language: str = "zh", parent: QWidget | None = None) -> None:
        super().__init__(parent); self.config = config or ThirdPartyFooterConfig(); self.language = language; self.setObjectName("thirdPartyFooter")
        self.setVisible(self.config.visible); self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed); self.setFixedHeight(38)
        layout = QHBoxLayout(self); layout.setContentsMargins(20, 0, 20, 0); layout.setSpacing(4); layout.addStretch()
        self.statement = QLabel(); self.statement.setObjectName("footerText"); self.help = QPushButton("?"); self.help.setObjectName("footerHelp"); self.help.setFixedSize(18, 18)
        layout.addWidget(self.statement); layout.addWidget(self.help); self.popover = DisclosurePopover(self.config, self)
        self.help.installEventFilter(self); self.set_language(language)

    def set_language(self, language: str) -> None:
        self.language = "zh" if language == "zh" else "en"; provider = self.config.provider_name
        self.statement.setText(f"本工具由第三方 {provider} 提供" if self.language == "zh" else f"This tool is provided by third-party {provider}")

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if watched is self.help:
            if event.type() == QEvent.Type.Enter: self.popover.show_for(self.help)
            elif event.type() == QEvent.Type.Leave: self.popover.hide_timer.start(180)
        return super().eventFilter(watched, event)
