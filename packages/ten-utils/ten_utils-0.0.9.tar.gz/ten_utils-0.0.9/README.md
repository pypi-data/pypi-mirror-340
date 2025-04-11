# 🧰 ten-utils

> A reusable Python toolkit for structured logging, configuration, and utilities — built for extensibility and clarity.

[![PyPI version](https://badge.fury.io/py/ten-utils.svg)](https://pypi.org/project/ten-utils/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)

---

## ✨ Features

- ✅ Structured and styled logging with `rich`
- 🔁 Singleton-based configuration manager
- 🧪 Clean testable architecture with `pytest`
- 📦 Easy to integrate into any project

---

## 📦 Installation

You can install `ten-utils` using pip:

```bash
pip install ten-utils
```

Or with development tools:

```bash
pip install ten-utils[dev]
```

---

## 🚀 Quick Start

```python
from ten_utils.log.logger import Logger
from ten_utils.log.config import LoggerConfig

# Set global configuration
LoggerConfig().set_default_level_log(1)       # INFO
LoggerConfig().set_save_log_to_file(False)    # Don't write to file

# Create logger instance
logger = Logger(name="MyApp")

# Logging
logger.debug("This is a debug message")     # Will be ignored (default = INFO)
logger.info("App started successfully")
logger.warning("This is a warning")
logger.error("An error occurred")
```

---

## ⚙️ Configuration

Use `LoggerConfig` to globally control logging behavior:

```python
from ten_utils.log.config import LoggerConfig

LoggerConfig().set_default_level_log(2)       # Set minimum level to WARNING
LoggerConfig().set_save_log_to_file(True)     # Enable file output
```

---

## 🧪 Running Tests

```bash
pytest tests/ --disable-warnings -v
```

To install test/dev dependencies:

```bash
pip install ten-utils[dev]
```

---

## 🧱 Project Structure

```text
ten_utils/
│
├── log/
│   ├── logger.py            # Main Logger class (Rich-powered)
│   ├── config.py            # Global logging configuration (Singleton)
│
├── common/
│   ├── decorators.py        # Decorators (e.g., log-level filter)
│   ├── constants.py         # Global constants for log levels and formats
│   ├── singleton.py         # Base singleton pattern implementation
│   ├── validators.py        # Input validation helpers
│
├── tests/                   # Unit tests
```

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Александр Караваев**  
[Email](mailto:234iskateli234@gmail.com)  
[GitHub Profile](https://github.com/Ten-o69)

---

## 💡 Contributing

Contributions, issues and feature requests are welcome!  
Feel free to open a [discussion](https://github.com/Ten-o69/ten-utils/discussions) or a [pull request](https://github.com/Ten-o69/ten-utils/pulls).

---
