# PySide6 Design Tokens

The executable source of truth is `shells/pyside6/src/ui_kit/tokens.py`.

| Token | Value | Use |
| --- | --- | --- |
| Background | `#0B0F17` | Window and content background |
| Surface | `#151B26` | Cards and sidebar |
| Primary | `#3730A3` | Primary actions and active navigation |
| Accent | `#D97706` | Warning state |
| Text | `#F3F4F6` | Primary text |
| Muted | `#9CA3AF` | Supporting text |
| Border | `#293241` | Card, input and shell borders |

Spacing tokens range from 4 to 32 px. Component radii are 6, 8 and 12 px.
Use `component_stylesheet()` rather than re-declaring these values in product pages.
