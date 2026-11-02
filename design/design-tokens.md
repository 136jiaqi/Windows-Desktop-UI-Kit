# PySide6 设计 Tokens / Design Tokens

可执行的唯一来源是 `shells/pyside6/src/ui_kit/tokens.py`。
The executable source of truth is `shells/pyside6/src/ui_kit/tokens.py`.

| Token / 名称 | Value / 值 | Use / 用途 |
| --- | --- | --- |
| Background / 主背景 | `#0B0F17` | Window and content background / 窗口与内容背景 |
| Surface / 表面 | `#151B26` | Cards and sidebar / 卡片与侧边栏 |
| Primary / 主色 | `#3730A3` | Primary actions and active navigation / 主操作与选中导航 |
| Accent / 强调色 | `#D97706` | Warning state / 警告状态 |
| Text / 主要文字 | `#F3F4F6` | Primary text / 主要文字 |
| Muted / 次要文字 | `#9CA3AF` | Supporting text / 辅助文字 |
| Border / 边框 | `#293241` | Card, input and shell borders / 卡片、输入框与外壳边框 |

间距 Tokens 为 4 至 32 px，组件圆角为 6、8、12 px。请使用 `component_stylesheet()`，不要在产品页面重复声明这些视觉值。
Spacing tokens range from 4 to 32 px. Component radii are 6, 8 and 12 px. Use `component_stylesheet()` rather than re-declaring these values in product pages.
