"""XMODhub launch guard shared by PySide6 tools."""

from __future__ import annotations

import subprocess

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QVBoxLayout, QWidget

XMODHUB_URL = "https://www.xmodhub.cn/"


def is_xmodhub_running() -> bool:
    """Return whether the Windows process list contains the XMODhub client."""
    if not hasattr(subprocess, "CREATE_NO_WINDOW"):
        return False
    result = subprocess.run(
        ["tasklist", "/FI", "IMAGENAME eq XMODhub.exe", "/NH", "/FO", "CSV"],
        capture_output=True,
        text=True,
        errors="replace",
        creationflags=subprocess.CREATE_NO_WINDOW,
        check=False,
    )
    return "xmodhub.exe" in result.stdout.lower()


class XmodhubRequiredDialog(QDialog):
    """A small, clickable error dialog shown when the host client is unavailable."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("XMODhub Required")
        self.setModal(True)
        self.setMinimumWidth(440)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(14)
        message = QLabel(
            f'请在XMODhub（下载地址：<a href="{XMODHUB_URL}">{XMODHUB_URL}</a>）中使用该工具！'
            f'<br><br>Please use this tool within XMODhub (download link: '
            f'<a href="{XMODHUB_URL}">{XMODHUB_URL}</a>)!'
        )
        message.setWordWrap(True)
        message.setTextFormat(Qt.TextFormat.RichText)
        message.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        message.setOpenExternalLinks(False)
        message.linkActivated.connect(lambda url: QDesktopServices.openUrl(QUrl(url)))
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(self.reject)
        buttons.accepted.connect(self.accept)
        layout.addWidget(message)
        layout.addWidget(buttons)


def require_xmodhub(parent: QWidget | None = None) -> bool:
    """Show the required-client error and return False when XMODhub is absent."""
    if is_xmodhub_running():
        return True
    XmodhubRequiredDialog(parent).exec()
    return False
