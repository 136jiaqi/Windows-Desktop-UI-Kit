---
name: windows-desktop-ui-kit
description: Build or modify a Windows PySide6 tool that reuses this repository's ShellWindow, components, i18n, Footer, and XMODhub launch guard. Use for product screens built on this UI kit; not for unrelated web or non-Windows UI work.
---

# Windows Desktop UI Kit

Use the repository's PySide6 shell as an imported dependency. Product code owns
business UI and data; the kit owns window chrome and shared presentation behavior.

## Before implementation

Read [`references/integration-rules.md`](references/integration-rules.md). Inspect
the existing `shells/pyside6/src/ui_kit` public API and the closest example before
changing code. Preserve user-owned changes and do not reinitialize Git.

## Build rules

- Use `ShellWindow` and inject a product widget via `set_content()`.
- Use `component_stylesheet()` and exported components. Keep visual constants in
  the UI kit's tokens, not inside product pages.
- Keep translation dictionaries in the product layer. Connect
  `window.language_changed` to a method that changes text on existing widgets.
  Do not recreate page controls, layouts, or the window to switch language.
- For XMODhub-distributed tools, call `require_xmodhub()` after creating the
  `QApplication` and before creating the product window.
- Use `ThirdPartyFooter` only when the product requires the configured disclosure;
  do not put product-specific provider text inside the shared component.
- Do not add game/system operations merely because an example contains simulated
  status data.

## Verification

Run Python compilation for the source and examples. For translation changes, verify
both languages and repeated switching without increasing child-widget counts or
changing the window size. For guarded tools, verify both process-detected and
process-missing paths without opening external links as part of automated tests.

Do not commit, push, publish, or build a release unless explicitly requested.
