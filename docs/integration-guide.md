# PySide6 集成指南 / Integration Guide

从 `ui_kit` 导入 `ShellWindow` 和产品实际需要的控件。产品控件独立维护，并通过 `window.set_content(product_widget)` 注入。Shell 只负责窗口外壳，不访问游戏进程、文件、注册表或业务配置。
Import `ShellWindow` and only the controls your product needs from `ui_kit`. Product widgets stay independent and are inserted with `window.set_content(product_widget)`. The shell owns window chrome only; it does not access game processes, files, registry, or configuration data.

```python
from ui_kit import PrimaryButton, ShellWindow, component_stylesheet

app.setStyleSheet(component_stylesheet())
window = ShellWindow("My Product")
window.set_content(MyProductPage())
window.apply_size_preset("small")  # 或 / or "large"
window.language_changed.connect(my_translation_controller.set_language)
window.show()
```

示例使用静态模拟数据。可复用其布局思路，但不要复制示例文案或伪数据模型。
The examples use static simulated data. Copy their layout ideas, not their product copy or fake data model.
