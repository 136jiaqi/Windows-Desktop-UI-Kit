"""Demo B: localized, simulated multi-page game assistant; no system access occurs."""

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication, QHBoxLayout, QLabel, QVBoxLayout, QWidget

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ui_kit import (Card, Dialog, FormInput, PrimaryButton, ProgressBar, ScrollArea,
                    SectionHeader, SecondaryButton, ShellWindow, SidebarNavigation, StatusBadge,
                    ThirdPartyFooter, ToggleSwitch, apply_text_map, component_stylesheet)
from ui_kit import require_xmodhub

COPY = {
    "zh": {"nav": [("overview", "概览"), ("fps", "FPS 性能评估"), ("environment", "环境检测"), ("settings", "设置")], "pages": {"overview": ("概览", "模拟运行状态与常用操作"), "fps": ("FPS 性能评估", "示例性能指标，不读取游戏进程"), "environment": ("环境检测", "示例环境状态，不执行系统扫描"), "settings": ("设置", "本页控件只在当前 Demo 内响应")}, "overview": [("助手状态", "模拟已就绪", "success"), ("模拟帧率", "144 FPS", "neutral"), ("环境提示", "1 项建议", "warning")], "quick": "快速操作（模拟）", "launch": "启动模拟评估", "report": "查看示例报告", "dialog_title": "模拟评估", "dialog_body": "已记录一个本地 Demo 操作；未启动或检查任何游戏。", "fps_card": "模拟帧时间稳定性", "fps_note": "82 / 100 · 静态示例数据，不采集硬件或游戏数据。", "env": [("图形运行库", "模拟就绪", "success"), ("游戏目录访问", "模拟状态", "neutral"), ("可选运行库", "建议检查", "warning")], "preferences": "Demo 偏好（仅本次运行）", "toggle": "显示性能悬浮提示", "config": "配置名称", "placeholder": "输入名称", "value": "默认游戏配置", "save": "保存 Demo 设置", "saved_title": "已保存", "saved_body": "设置仅在当前运行的 Demo 内展示。"},
    "en": {"nav": [("overview", "Overview"), ("fps", "FPS Assessment"), ("environment", "Environment"), ("settings", "Settings")], "pages": {"overview": ("Overview", "Simulated status and common actions"), "fps": ("FPS Assessment", "Sample performance data; no game process is read"), "environment": ("Environment", "Sample status only; no system scan is run"), "settings": ("Settings", "Controls respond only inside this demo")}, "overview": [("Assistant", "Simulation ready", "success"), ("Sample FPS", "144 FPS", "neutral"), ("Environment", "1 suggestion", "warning")], "quick": "Quick actions (simulated)", "launch": "Run simulated assessment", "report": "View sample report", "dialog_title": "Simulated assessment", "dialog_body": "A local demo action was recorded. No game was launched or inspected.", "fps_card": "Simulated frame-time stability", "fps_note": "82 / 100 · Static sample data; no hardware or game data is collected.", "env": [("Graphics runtime", "Sample ready", "success"), ("Game directory access", "Simulated", "neutral"), ("Optional runtime", "Review", "warning")], "preferences": "Demo preferences (this session only)", "toggle": "Show performance overlay", "config": "Configuration name", "placeholder": "Enter a name", "value": "Default game profile", "save": "Save demo settings", "saved_title": "Saved", "saved_body": "Settings are shown only in this running demo."},
}


class AssistantPage(QWidget):
    def __init__(self, language: str = "zh") -> None:
        super().__init__(); self.setObjectName("contentPage"); self.language = language; self.current_key = "overview"
        self.root = QHBoxLayout(self); self.root.setContentsMargins(0, 0, 0, 0); self.root.setSpacing(0)
        self.scroll_content = QWidget(); self.scroll_content.setObjectName("contentPage")
        self.content_layout = QVBoxLayout(self.scroll_content); self.content_layout.setContentsMargins(28, 24, 28, 28); self.content_layout.setSpacing(16)
        self.scroll = ScrollArea(self.scroll_content); self.footer = ThirdPartyFooter(language=language)
        self.right = QWidget(); self.right.setObjectName("contentPage"); right_layout = QVBoxLayout(self.right); right_layout.setContentsMargins(0, 0, 0, 0); right_layout.setSpacing(0); right_layout.addWidget(self.scroll, 1); right_layout.addWidget(self.footer)
        self.build_navigation(); self.root.addWidget(self.nav); self.root.addWidget(self.right, 1); self.show_page(self.current_key)

    def build_navigation(self) -> None:
        if hasattr(self, "nav"):
            self.root.removeWidget(self.nav); self.nav.deleteLater()
        self.nav = SidebarNavigation(COPY[self.language]["nav"]); self.nav.changed.connect(self.show_page)

    def set_language(self, language: str) -> None:
        if language == self.language:
            return
        old, new = COPY[self.language], COPY[language]
        text_map: dict[str, str] = {}
        for old_item, new_item in zip(old["nav"], new["nav"]):
            text_map[old_item[1]] = new_item[1]
        for key in old["pages"]:
            text_map[old["pages"][key][0]] = new["pages"][key][0]
            text_map[old["pages"][key][1]] = new["pages"][key][1]
        for key in ("quick", "launch", "report", "fps_card", "fps_note", "preferences", "toggle", "config", "placeholder", "value", "save"):
            text_map[old[key]] = new[key]
        for old_item, new_item in zip(old["overview"], new["overview"]):
            text_map[old_item[0]] = new_item[0]; text_map[old_item[1]] = new_item[1]
        for old_item, new_item in zip(old["env"], new["env"]):
            text_map[old_item[0]] = new_item[0]; text_map[old_item[1]] = new_item[1]
        self.language = language
        apply_text_map(self, text_map)
        self.footer.set_language(language)

    def show_page(self, key: str) -> None:
        self.current_key = key
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        t = COPY[self.language]; title, subtitle = t["pages"][key]; self.content_layout.addWidget(SectionHeader(title, subtitle))
        if key == "overview": self._overview(t)
        elif key == "fps": self._fps(t)
        elif key == "environment": self._environment(t)
        else: self._settings(t)
        self.content_layout.addStretch()

    def _overview(self, t: dict) -> None:
        row = QHBoxLayout(); row.setSpacing(12)
        for name, value, tone in t["overview"]:
            card = Card(); card.layout.addWidget(QLabel(name)); card.layout.addWidget(StatusBadge(value, tone)); row.addWidget(card, 1)
        self.content_layout.addLayout(row)
        actions = Card(); actions.layout.addWidget(QLabel(t["quick"])); buttons = QHBoxLayout(); launch = PrimaryButton(t["launch"])
        launch.clicked.connect(self.show_assessment_dialog)
        buttons.addWidget(launch); buttons.addWidget(SecondaryButton(t["report"])); buttons.addStretch(); actions.layout.addLayout(buttons); self.content_layout.addWidget(actions)

    def _fps(self, t: dict) -> None:
        card = Card(); card.layout.addWidget(QLabel(t["fps_card"])); card.layout.addWidget(ProgressBar(82)); note = QLabel(t["fps_note"]); note.setObjectName("mutedText"); note.setWordWrap(True); card.layout.addWidget(note); self.content_layout.addWidget(card)
        for label in ("Average FPS: 144 (simulated)", "1% Low: 98 (simulated)", "Frame time: 6.9 ms (simulated)"):
            item = Card(); item.layout.addWidget(QLabel(label)); self.content_layout.addWidget(item)

    def _environment(self, t: dict) -> None:
        for name, badge, tone in t["env"]:
            item = Card(); row = QHBoxLayout(); row.addWidget(QLabel(name)); row.addStretch(); row.addWidget(StatusBadge(badge, tone)); item.layout.addLayout(row); self.content_layout.addWidget(item)

    def _settings(self, t: dict) -> None:
        card = Card(); card.layout.addWidget(QLabel(t["preferences"])); line = QHBoxLayout(); line.addWidget(QLabel(t["toggle"])); line.addStretch(); line.addWidget(ToggleSwitch(True)); card.layout.addLayout(line)
        card.layout.addWidget(QLabel(t["config"])); card.layout.addWidget(FormInput(t["placeholder"], t["value"])); save = PrimaryButton(t["save"]); save.clicked.connect(self.show_saved_dialog); card.layout.addWidget(save); self.content_layout.addWidget(card)

    def show_assessment_dialog(self) -> None:
        t = COPY[self.language]; Dialog(t["dialog_title"], t["dialog_body"], self).exec()

    def show_saved_dialog(self) -> None:
        t = COPY[self.language]; Dialog(t["saved_title"], t["saved_body"], self).exec()


if __name__ == "__main__":
    app = QApplication(sys.argv); app.setStyleSheet(component_stylesheet())
    if not require_xmodhub():
        raise SystemExit(0)
    window = ShellWindow("Game Assistant"); page = AssistantPage(window.language_manager.language)
    window.set_content(page); window.language_changed.connect(page.set_language); window.apply_size_preset("large"); window.show()
    raise SystemExit(app.exec())
