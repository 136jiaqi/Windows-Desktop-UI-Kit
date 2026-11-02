"""Central design tokens and the shared Qt style sheet."""

from __future__ import annotations

COLORS = {
    "background": "#0B0F17", "surface": "#151B26", "surface_hover": "#1C2431",
    "primary": "#3730A3", "primary_hover": "#4F46E5", "accent": "#D97706",
    "text": "#F3F4F6", "muted": "#9CA3AF", "border": "#293241",
    "success": "#16A34A", "warning": "#D97706", "danger": "#DC2626",
}

RADIUS = {"small": 6, "medium": 8, "large": 12}
SPACING = {"xs": 4, "sm": 8, "md": 12, "lg": 18, "xl": 24, "xxl": 32}


def component_stylesheet() -> str:
    """Return the shared component style sheet; no page owns visual tokens."""
    c = COLORS
    return f"""
        QWidget {{ color: {c['text']}; font-family: 'Segoe UI', 'Microsoft YaHei UI'; font-size: 13px; }}
        QWidget#contentPage {{ background: {c['background']}; }}
        QFrame#card {{ background: {c['surface']}; border: 1px solid {c['border']}; border-radius: 10px; }}
        QLabel#sectionTitle {{ font-size: 18px; font-weight: 600; color: {c['text']}; }}
        QLabel#sectionSubtitle, QLabel#mutedText {{ color: {c['muted']}; }}
        QPushButton#primaryButton {{ background: {c['primary']}; border: 1px solid {c['primary']}; border-radius: 7px; padding: 0 14px; min-height: 36px; font-size: 13px; font-weight: 600; color: white; }}
        QPushButton#primaryButton:hover {{ background: {c['primary_hover']}; }}
        QPushButton#primaryButton:pressed {{ background: #2E278A; }}
        QPushButton#primaryButton:disabled, QPushButton#secondaryButton:disabled, QPushButton#iconButton:disabled {{ background: #202938; color: #667085; border-color: #202938; }}
        QPushButton#secondaryButton {{ background: transparent; border: 1px solid {c['border']}; border-radius: 7px; padding: 0 14px; min-height: 36px; font-size: 13px; color: {c['text']}; }}
        QPushButton#secondaryButton:hover, QPushButton#iconButton:hover {{ background: {c['surface_hover']}; border-color: #46556A; }}
        QPushButton#secondaryButton:pressed, QPushButton#iconButton:pressed {{ background: #111823; }}
        QPushButton#iconButton {{ background: transparent; border: 1px solid {c['border']}; border-radius: 7px; min-width: 36px; max-width: 36px; min-height: 36px; font-size: 15px; }}
        QPushButton#sidebarItem {{ background: transparent; border: 0; border-radius: 7px; min-height: 36px; padding: 0 12px; text-align: left; color: {c['muted']}; }}
        QPushButton#sidebarItem:hover {{ background: {c['surface_hover']}; color: {c['text']}; }}
        QPushButton#sidebarItem:checked {{ background: #242040; color: {c['text']}; font-weight: 600; }}
        QPushButton#languageButton {{ min-width: 58px; padding: 0 8px; border-radius: 5px; }}
        QLineEdit#formInput {{ background: #101722; border: 1px solid {c['border']}; border-radius: 7px; padding: 0 10px; min-height: 34px; selection-background-color: {c['primary']}; }}
        QLineEdit#formInput:focus {{ border-color: {c['primary_hover']}; }}
        QScrollArea#scrollArea {{ background: transparent; border: 0; }}
        QScrollBar:vertical {{ background: transparent; width: 10px; margin: 4px; }}
        QScrollBar::handle:vertical {{ background: #3A4658; border-radius: 4px; min-height: 28px; }}
        QScrollBar::handle:vertical:hover {{ background: #536177; }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
        QProgressBar {{ background: #101722; border: 1px solid {c['border']}; border-radius: 5px; height: 10px; text-align: center; color: transparent; }}
        QProgressBar::chunk {{ background: {c['primary']}; border-radius: 4px; }}
        QCheckBox#toggle {{ spacing: 0; }} QCheckBox#toggle::indicator {{ width: 36px; height: 20px; border-radius: 10px; background: #3A4658; }}
        QCheckBox#toggle::indicator:checked {{ background: {c['primary_hover']}; }}
        QDialog {{ background: {c['surface']}; }}
        QWidget#thirdPartyFooter {{ background: {c['background']}; }}
        QLabel#footerText {{ color: {c['muted']}; font-size: 11px; }}
        QLabel#footerLink {{ font-size: 11px; }} QLabel#footerLink a {{ color: #A5B4FC; text-decoration: none; }}
        QPushButton#footerHelp {{ background: #293241; border: 0; border-radius: 9px; color: {c['text']}; font-size: 11px; font-weight: 600; padding: 0; }}
        QPushButton#footerHelp:hover {{ background: #46556A; }}
        QFrame#disclosurePopover {{ background: #151B26; color: {c['text']}; border: 1px solid #46556A; border-radius: 8px; }}
        QFrame#disclosurePopover QLabel {{ color: {c['text']}; font-size: 12px; }} QFrame#disclosurePopover a {{ color: #A5B4FC; }}
    """
