# Windows Desktop UI Kit

适用于 AI 辅助开发 Windows 桌面 EXE 的可复用窗口外壳。
Reusable, Windows-focused shells for AI-assisted desktop EXE projects.

## v0.1.0 状态 / Status

当前已提供 `shells/pyside6` 中的 PySide6 基础外壳：深色无边框窗口、可复用标题栏、原生系统拖动/缩放，以及明确的内容注入接口。项目不包含游戏或产品业务逻辑。
The PySide6 base shell is available in `shells/pyside6`: a dark frameless window, a reusable title bar, native system move/resize behavior, and a content-insertion interface. It deliberately contains no game or product logic.

查看 [PySide6 Shell 说明](shells/pyside6/README.md) 了解启动与集成方式。
See [the PySide6 shell README](shells/pyside6/README.md) for startup and integration instructions.

进行 AI 辅助开发前，请先阅读 [AI_INSTRUCTIONS.md](AI_INSTRUCTIONS.md)。可复用 Agent Skill 位于 [`agent-skills/windows-desktop-ui-kit`](agent-skills/windows-desktop-ui-kit/)。
For AI-assisted development, start with [AI_INSTRUCTIONS.md](AI_INSTRUCTIONS.md). The reusable Agent Skill is stored in [`agent-skills/windows-desktop-ui-kit`](agent-skills/windows-desktop-ui-kit/).
