# AI 集成说明 / AI Integration Instructions

将本仓库作为 Windows 桌面工具外壳的唯一规范来源。创建或修改使用本套件的 PySide6 工具前，请先阅读 [`agent-skills/windows-desktop-ui-kit/SKILL.md`](agent-skills/windows-desktop-ui-kit/SKILL.md)。
Use this repository as the source of truth for Windows desktop tool shells. Read [`agent-skills/windows-desktop-ui-kit/SKILL.md`](agent-skills/windows-desktop-ui-kit/SKILL.md) before creating or changing a PySide6 tool that uses this kit.

## 必须遵守的集成规则 / Non-negotiable integration rules

- 复用 `ShellWindow`；不要在业务代码中再实现自定义标题栏、窗口拖动、缩放、最大化或语言持久化。
  Reuse `ShellWindow`; do not create a second custom title bar or implement window drag, resize, maximize, or language persistence in product code.
- 将产品 UI 作为独立控件，通过 `window.set_content()` 注入。
  Create product UI as a separate widget and supply it with `window.set_content()`.
- 每个 `QApplication` 仅应用一次 `component_stylesheet()`，并使用导出的组件与 Tokens。
  Apply `component_stylesheet()` once per `QApplication` and use exported UI-kit components/tokens instead of page-local visual constants.
- 将 `ShellWindow.language_changed` 连接至原地更新已有控件的页面方法，不要仅为翻译重建页面。
  Connect `ShellWindow.language_changed` to a page method that updates existing widgets in place. Do not rebuild a page merely to translate it.
- 通过 XMODhub 分发的工具必须在创建主窗口前调用 `require_xmodhub()`。
  Tools distributed through XMODhub must call `require_xmodhub()` before creating their main window.
- Demo 数据必须明确标记为模拟数据；除非已实现且获得授权，不得声称实际执行系统或游戏操作。
  Demo data must be visibly labelled simulated. Do not claim real system/game operations unless those operations were specifically implemented and authorized.
- 未获得用户明确请求时，不要提交、推送、打包或发布。
  Do not commit, push, package, or publish unless the user explicitly requests it.

新工具请从 [`templates/pyside6_tool_entry.py`](templates/pyside6_tool_entry.py) 开始，并按需查阅集成指南。
Start from [`templates/pyside6_tool_entry.py`](templates/pyside6_tool_entry.py) for a new tool entry point, then consult the integration guide as needed.
