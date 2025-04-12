# PyAddRoute 🌐

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A Python GUI tool for managing network routes on Windows systems. Supports both IPv4 and IPv6 routes with an intuitive interface.

## 🚀 Features

- Intuitive GUI interface for managing network routes
- Full support for both IPv4 and (IPv6 routes, not yet)
- View, add, modify, and delete routes
- Display interface metrics and network details
- Real-time route table updates
- Windows OS support
- Lightweight and efficient

## 📦 Installation

```bash
pip install pyaddroute
```

Or using UV (recommended):

```bash
uv pip install pyaddroute
```

## 🖥️ Usage Example

Simply run the command:

```bash
pyaddroute
```

Or run as a module:

```bash
python -m pyaddroute
```

## 🖼️ Screenshot

![PyAddRoute Interface](screenshot.png)

## 📋 Requirements

- Python 3.8 or later
- Windows operating system
- Administrator privileges (for route management)

Dependencies are managed through `pyproject.toml`:
- FreeSimpleGUI >= 4.60.0
- loguru >= 0.7.0

## 🔐 Permissions

Administrator privileges are required to modify network routes on Windows systems.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📫 Contact

If you have any questions or suggestions, please open an issue in the repository.

---

<div align="center">
Made with ❤️ using Python
</div>