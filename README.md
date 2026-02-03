# 📦 hxppy-archivator

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**hxppy-archivator** — это легкая CLI-утилита для упаковки всего вашего исходного кода в один читаемый текстовый файл и его последующей мгновенной распаковки.

### 🚀 Зачем это нужно?
- **LLM Context:** Идеальный способ передать весь ваш проект в ChatGPT или Claude одним файлом.
- **Backups:** Быстрые текстовые слепки кода.
- **Smart:** Автоматически уважает ваш `.gitignore` и не тянет лишний мусор (node_modules, .venv, etc.).

## 🛠 Установка

```bash
git clone [https://github.com/HxppyCompany/hxppy-archivator.git](https://github.com/HxppyCompany/hxppy-archivator.git)
cd hxppy-archivator
pip install -e .
