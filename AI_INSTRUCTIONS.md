# AI Integration Instructions

Use this repository as the source of truth for Windows desktop tool shells. Read
[`agent-skills/windows-desktop-ui-kit/SKILL.md`](agent-skills/windows-desktop-ui-kit/SKILL.md)
before creating or changing a PySide6 tool that uses this kit.

## Non-negotiable integration rules

- Reuse `ShellWindow`; do not create a second custom title bar or implement window
  drag, resize, maximize, or language persistence in product code.
- Create product UI as a separate widget and supply it with `window.set_content()`.
- Apply `component_stylesheet()` once per `QApplication` and use exported UI-kit
  components/tokens instead of page-local visual constants.
- Connect `ShellWindow.language_changed` to a page method that updates existing
  widgets in place. Do not rebuild a page merely to translate it.
- Tools distributed through XMODhub must call `require_xmodhub()` before creating
  their main window.
- Demo data must be visibly labelled simulated. Do not claim real system/game
  operations unless those operations were specifically implemented and authorized.
- Do not commit, push, package, or publish unless the user explicitly requests it.

Start from [`templates/pyside6_tool_entry.py`](templates/pyside6_tool_entry.py) for
a new tool entry point, then consult the integration guide as needed.
