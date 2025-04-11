# ProjectPlyra

> A modern, one-liner visualization library built on top of Plotly.

**Plyra** gives you the power of Plotly with the simplicity of Seaborn. It's built for developers, data scientists, and learners who want beautiful interactive plots with minimal code.

###### One liner: seaborn-style code, but interactive graphs

---

## 🔧 Features

- Built on `plotly.express` and `plotly.graph_objects`
- One-liner plotting: `scatter`, `hist`, `bar`, `box`, `kde`, `heatmap`, `countplot`
- Easy theming (`plotly`, `ggplot2`, `plotly_dark`, etc.)
- Utilities for merging plots (`Utils.join`)
- Supports `additional_updates` for fine-grained customization

---

## 🚀 Installation

```bash
pip install plyra
```

## 🧪 Quick Example
```python
import plyra as pl
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "age": np.random.randint(10, 60, 100),
    "score": np.random.normal(75, 10, 100),
    "gender": np.random.choice(["Male", "Female"], 100)
})

pl.set_theme("ggplot2")
fig = pl.scatter(df, x="age", y="score", color="gender")
fig.show()
```
---
## 📊 Plot Types
Plot: Function
Scatter: `pl.scatter()`
Histogram: `pl.hist()`
KDE: `pl.kde()`
Bar: `pl.bar()` / `pl.barh()`
Box: `pl.box()`
Heatmap: `pl.heatmap()`
Count: `pl.countplot()`

---
## 🔍 Fine-tuning Your Plot
All plot functions accept:

```python
additional_updates = {
    "layout": {"title_font_size": 24},
    "xaxis": {"tickangle": -45}
}
```
Use them for full customization without writing messy code.

---
## 🧠 Want to Join?
Plyra is indie-built and open-source.
Feel free to fork, contribute, or suggest features.

## 📄 License
[MIT License](LICENSE)