# PySide6 Shell Integration Rules

## Public entry points

Import from `ui_kit`, not individual internal modules where possible:

- `ShellWindow`: frameless shell, title bar, persisted language state and size presets.
- `component_stylesheet()`: application-wide shared appearance.
- `PrimaryButton`, `SecondaryButton`, `Card`, `StatusBadge`, `ScrollArea`, and other
  exported controls: reuse these before creating product-local variants.
- `ThirdPartyFooter` and `ThirdPartyFooterConfig`: optional fixed disclosure footer.
- `require_xmodhub()`: Windows process guard for XMODhub-only tools.

## Language flow

`ShellWindow.language_changed` emits `zh` or `en`. A product page must retain its
widgets and update their `text`, `placeholderText`, badges and visible footer in
place. Once texts change, invalidate/activate the relevant layouts and call
`updateGeometry()` if the page does not use the provided `apply_text_map()` helper.

Do not add translated `QLabel` or `QPushButton` instances over old controls. Do not
rebuild an entire page on a language-only change.

## XMODhub-only startup

Create `QApplication`, apply the style sheet, then call `require_xmodhub()`. If it
returns false, exit before constructing the main window. The guard shows the shared
download dialog and opens its link through the system browser.

## Layout

Use Qt layouts for all product UI. A fixed Footer belongs outside the content
`ScrollArea`; the scroll area is the expanding layout item. Do not position primary
content with `move()` or `setGeometry()`.
