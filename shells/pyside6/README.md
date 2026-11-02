# PySide6 Shell

## Run the demos

```bat
cd shells\pyside6
py -m pip install -r requirements.txt
py examples\stage_one_demo.py
py examples\single_page_tool_demo.py
py examples\sidebar_tool_demo.py
```

## Reuse in a product

Put `src` on the Python path, create `ShellWindow`, then inject a product-owned
widget with `set_content`. The shell deliberately owns only title-bar and window
behavior.

```python
window = ShellWindow("My Tool")
window.set_content(MyToolPage())
window.show()
```

Use `window.apply_size_preset("small")` for a compact tool window (900 × 620),
or `window.apply_size_preset("large")` for a comprehensive tool window (1180 × 760).

## Components

Import components from `ui_kit`: `PrimaryButton`, `SecondaryButton`, `IconButton`,
`SidebarNavigation`, `Card`, `StatusBadge`, `ToggleSwitch`, `ProgressBar`,
`ScrollArea`, `Dialog`, `FormInput`, and `SectionHeader`. Shared color, spacing and
corner tokens are in `ui_kit.tokens`; apply `component_stylesheet()` once at app start.

`ShellWindow.language_changed` emits `zh` or `en` when the built-in language
selector is clicked. The selection is persisted with `QSettings`; when no saved
choice exists, `zh-CN` and `zh-SG` start in Chinese and all other locales in English.

## Current Windows behavior

- Frameless Qt window; no native title bar is retained.
- Empty title-bar space starts Qt's native `startSystemMove`, enabling normal drag
  and Windows Snap for drag gestures.
- Border/corner clicks use Qt's native `startSystemResize` (normal window state).
- `showMaximized()` uses Windows' available work area, so the taskbar is not covered.
- Minimize, maximize/restore, close, Alt+F4, high-DPI scaling, and taskbar restore
  use normal Qt/Windows behavior.

Windows 11's hover Snap Layout flyout on the custom maximize button is not available
through this pure Qt widget implementation: the button is an application control,
not the OS caption button. Drag-to-snap remains available.
