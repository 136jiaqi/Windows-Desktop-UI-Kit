# PySide6 Integration Guide

Import `ShellWindow` and only the controls your product needs from `ui_kit`. Product
widgets stay independent and are inserted with `window.set_content(product_widget)`.
The shell owns window chrome only; it does not access game processes, files, registry,
or configuration data.

```python
from ui_kit import PrimaryButton, ShellWindow, component_stylesheet

app.setStyleSheet(component_stylesheet())
window = ShellWindow("My Product", language="简中")
window.set_content(MyProductPage())
window.apply_size_preset("small")  # or "large"
window.language_changed.connect(my_translation_controller.set_language)
window.show()
```

The examples use static simulated data. Copy their layout ideas, not their product
copy or fake data model.
