"""Demo A: localized, simulated game-environment repair layout; performs no system work."""

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import QApplication, QGridLayout, QHBoxLayout, QLabel, QVBoxLayout, QWidget

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ui_kit import (Card, Dialog, PrimaryButton, ProgressBar, ScrollArea, SectionHeader,
                    SecondaryButton, ShellWindow, StatusBadge, ThirdPartyFooter, apply_text_map, component_stylesheet)
from ui_kit import require_xmodhub

COPY = {
    "zh": {"title": "游戏环境修复", "subtitle": "模拟数据演示：不会读取、检查或修改 Windows 系统。", "summary": "模拟环境状态", "ready": "3 项就绪", "scan": "开始模拟检测", "repair": "模拟修复", "progress": "模拟检测进度", "log": "执行日志（模拟）", "idle": "• Demo 已就绪，等待模拟操作。\n• 所有状态均为示例数据。", "scanning": "• 正在运行模拟检测…\n• 未访问注册表、文件或系统设置。", "done": "• 模拟检测完成，无需真实修复。\n• 所有结果均为模拟数据。", "dialog_title": "模拟操作", "dialog_body": "修复功能仅用于演示，不会修改 Windows 系统。", "checks": [("DirectX Runtime", "已就绪", "success"), ("Microsoft Visual C++", "已就绪", "success"), (".NET Desktop Runtime", "建议检查", "warning"), ("系统 DLL", "已就绪", "success")]},
    "en": {"title": "Game Environment Repair", "subtitle": "Simulated data only. This demo does not inspect or modify Windows.", "summary": "Simulated environment", "ready": "3 ready", "scan": "Run simulated scan", "repair": "Simulate repair", "progress": "Simulated scan progress", "log": "Activity log (simulated)", "idle": "• Demo is ready.\n• Every status below is sample data.", "scanning": "• Running a simulated scan…\n• No registry, file, or system settings are accessed.", "done": "• Simulated scan complete; no real repair was run.\n• Every result is simulated.", "dialog_title": "Simulated action", "dialog_body": "Repair is a visual demo only and will not modify Windows.", "checks": [("DirectX Runtime", "Ready", "success"), ("Microsoft Visual C++", "Ready", "success"), (".NET Desktop Runtime", "Review", "warning"), ("System DLL", "Ready", "success")]},
}


class RepairPage(QWidget):
    def __init__(self, language: str = "zh") -> None:
        super().__init__(); self.setObjectName("contentPage")
        self.language = language; self._progress_value = 0; self.timer = QTimer(self); self.timer.timeout.connect(self._step)
        root = QVBoxLayout(self); root.setContentsMargins(0, 0, 0, 0); root.setSpacing(0)
        self.body = QWidget(); self.body.setObjectName("contentPage")
        self.outer = QVBoxLayout(self.body); self.outer.setContentsMargins(28, 24, 28, 20); self.outer.setSpacing(18)
        self.footer = ThirdPartyFooter(language=language)
        root.addWidget(ScrollArea(self.body), 1); root.addWidget(self.footer)
        self.build()

    def build(self) -> None:
        while self.outer.count():
            item = self.outer.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        t = COPY[self.language]
        self.outer.addWidget(SectionHeader(t["title"], t["subtitle"]))
        summary = Card(); header = QHBoxLayout(); header.addWidget(QLabel(t["summary"])); header.addStretch(); header.addWidget(StatusBadge(t["ready"], "success")); summary.layout.addLayout(header)
        grid = QGridLayout(); grid.setHorizontalSpacing(18); grid.setVerticalSpacing(12); grid.setColumnStretch(0, 1); grid.setColumnStretch(2, 1)
        for index, (name, state, tone) in enumerate(t["checks"]):
            item = QLabel(name); item.setStyleSheet("font-weight: 600;")
            badge = StatusBadge(state, tone); row, col = index // 2, (index % 2) * 2
            grid.addWidget(item, row, col); grid.addWidget(badge, row, col + 1, Qt.AlignmentFlag.AlignRight)
        summary.layout.addLayout(grid); self.outer.addWidget(summary)
        actions = QHBoxLayout(); self.scan = PrimaryButton(t["scan"]); self.repair = SecondaryButton(t["repair"])
        self.scan.clicked.connect(self.run_scan); self.repair.clicked.connect(self.show_repair_dialog)
        actions.addWidget(self.scan); actions.addWidget(self.repair); actions.addStretch(); self.outer.addLayout(actions)
        progress_card = Card(); progress_card.layout.addWidget(QLabel(t["progress"])); self.progress = ProgressBar(self._progress_value); progress_card.layout.addWidget(self.progress); self.outer.addWidget(progress_card)
        log_card = Card(); log_card.layout.addWidget(QLabel(t["log"])); self.log = QLabel(t["idle"]); self.log.setObjectName("mutedText"); self.log.setWordWrap(True); log_card.layout.addWidget(self.log); self.outer.addWidget(log_card); self.outer.addStretch()

    def set_language(self, language: str) -> None:
        if language == self.language:
            return
        old, new = COPY[self.language], COPY[language]
        keys = ("title", "subtitle", "summary", "ready", "scan", "repair", "progress", "log", "idle", "scanning", "done")
        text_map = {old[key]: new[key] for key in keys}
        for old_item, new_item in zip(old["checks"], new["checks"]):
            text_map[old_item[0]] = new_item[0]
            text_map[old_item[1]] = new_item[1]
        self.language = language
        apply_text_map(self.body, text_map)
        self.footer.set_language(language)

    def run_scan(self) -> None:
        self._progress_value = 0; self.progress.setValue(0); self.scan.setDisabled(True); self.log.setText(COPY[self.language]["scanning"]); self.timer.start(90)

    def show_repair_dialog(self) -> None:
        t = COPY[self.language]
        Dialog(t["dialog_title"], t["dialog_body"], self).exec()

    def _step(self) -> None:
        self._progress_value += 8; self.progress.setValue(self._progress_value)
        if self._progress_value >= 100:
            self.timer.stop(); self.scan.setDisabled(False); self.log.setText(COPY[self.language]["done"])


if __name__ == "__main__":
    app = QApplication(sys.argv); app.setStyleSheet(component_stylesheet())
    if not require_xmodhub():
        raise SystemExit(0)
    window = ShellWindow("Windows Game Environment Tool"); page = RepairPage(window.language_manager.language)
    window.set_content(page); window.language_changed.connect(page.set_language); window.apply_size_preset("small"); window.show()
    raise SystemExit(app.exec())
