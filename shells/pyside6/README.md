# PySide6 外壳 / PySide6 Shell

## 运行 Demo / Run the demos

```bat
cd shells\pyside6
py -m pip install -r requirements.txt
py examples\stage_one_demo.py
py examples\single_page_tool_demo.py
py examples\sidebar_tool_demo.py
```

当前 Demo 需要检测到 `XMODhub.exe` 进程才会创建主窗口；未检测到时会显示下载提示弹窗。
The current demos create their main window only when the `XMODhub.exe` process is detected; otherwise they show a download prompt.

## 在产品中复用 / Reuse in a product

将 `src` 放入 Python 路径，创建 `ShellWindow`，再使用 `set_content` 注入产品控件。Shell 只负责标题栏和窗口行为。
Put `src` on the Python path, create `ShellWindow`, then inject a product-owned widget with `set_content`. The shell deliberately owns only title-bar and window behavior.

```python
window = ShellWindow("My Tool")
window.set_content(MyToolPage())
window.show()
```

紧凑工具窗口使用 `window.apply_size_preset("small")`（900 × 620）；综合工具窗口使用 `window.apply_size_preset("large")`（1180 × 760）。
Use `window.apply_size_preset("small")` for a compact tool window (900 × 620), or `window.apply_size_preset("large")` for a comprehensive tool window (1180 × 760).

## 组件 / Components

从 `ui_kit` 导入 `PrimaryButton`、`SecondaryButton`、`IconButton`、`SidebarNavigation`、`Card`、`StatusBadge`、`ToggleSwitch`、`ProgressBar`、`ScrollArea`、`Dialog`、`FormInput` 和 `SectionHeader`。共享颜色、间距与圆角位于 `ui_kit.tokens`；每个应用启动时只需应用一次 `component_stylesheet()`。
Import components from `ui_kit`: `PrimaryButton`, `SecondaryButton`, `IconButton`, `SidebarNavigation`, `Card`, `StatusBadge`, `ToggleSwitch`, `ProgressBar`, `ScrollArea`, `Dialog`, `FormInput`, and `SectionHeader`. Shared color, spacing and corner tokens are in `ui_kit.tokens`; apply `component_stylesheet()` once at app start.

点击内置语言按钮时，`ShellWindow.language_changed` 会发出 `zh` 或 `en`。选择通过 `QSettings` 保存；无保存值时，`zh-CN` 与 `zh-SG` 默认中文，其他系统语言默认英文。
`ShellWindow.language_changed` emits `zh` or `en` when the built-in language selector is clicked. The selection is persisted with `QSettings`; when no saved choice exists, `zh-CN` and `zh-SG` start in Chinese and all other locales in English.

## 当前 Windows 行为 / Current Windows behavior

- 无边框 Qt 窗口，不保留系统原生标题栏。 / Frameless Qt window; no native title bar is retained.
- 标题栏空白区域使用原生 `startSystemMove`，支持拖动和 Windows Snap。 / Empty title-bar space starts native `startSystemMove`, enabling normal drag and Windows Snap.
- 边缘与四角使用原生 `startSystemResize`。 / Border and corner clicks use native `startSystemResize`.
- `showMaximized()` 使用 Windows 可用工作区，不遮挡任务栏。 / `showMaximized()` uses Windows' available work area, so the taskbar is not covered.
- 最小化、最大化/还原、关闭、Alt+F4、高 DPI 与任务栏恢复使用 Qt/Windows 标准行为。 / Minimize, maximize/restore, close, Alt+F4, high-DPI scaling, and taskbar restore use normal Qt/Windows behavior.

Windows 11 自定义最大化按钮无法显示系统原生 Snap Layout 悬停浮层；仍可通过拖拽窗口进行 Snap。
Windows 11's hover Snap Layout flyout on the custom maximize button is unavailable in this pure Qt implementation; drag-to-snap remains available.
