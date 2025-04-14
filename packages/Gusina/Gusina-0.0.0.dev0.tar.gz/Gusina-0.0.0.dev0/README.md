# Gusina Engine

![PyPI version](https://img.shields.io/pypi/v/Gusina.svg)
![Development Status](https://img.shields.io/badge/status-planning-lightgrey.svg)
![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)

> **Gusina** - light and easy engine
> Development started on 13/04/2025.

---

## 📖 Description

Gusina — is a minimalist engine on Python 2.7 / 3.x, which allows you to quickly prototype scenes using a simple API:

```python
from gusina.core import GusinaBase, Entity, color

app = GusinaBase()
Entity(form='cube', color=color.red, pos=(0,0,0))
app.run()