[![Use this template](https://img.shields.io/badge/-Use%20this%20template-brightgreen?style=for-the-badge)](https://github.com/adhikaripb/protocol-formatter/generate)
<p align="center">
  <img src="assets/banner.png" width="80%" alt="Repo Banner"/>
</p>
# 🧾 Protocol Formatter

**Format raw text protocols into clean, publish-ready Word and pdf documents**  
Say goodbye to messy indentation, unclear bulleting, and formatting inconsistency in step-by-step protocols.

---


[![PyPI version](https://img.shields.io/pypi/v/protocol-formatter?color=blue)](https://pypi.org/project/protocol-formatter/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
![Python version](https://img.shields.io/badge/python-3.7%2B-blue)
![Status](https://img.shields.io/badge/status-active-brightgreen)

---

## ✨ Features

- Automatically detects stepwise sections in `.txt` protocols
- Adds clean spacing between blocks
- Handles blank lines, indents, and bullet lists
- Formats output to a well-structured `.docx` document
- Output file uses the same name as input (with `.docx` extension)
- Fully local and fast

---

## 📦 Installation

```bash
pip install protocol-formatter
```
> **Note for macOS/Linux users**:  
> This package relies on system-level libraries like Cairo, Pango, and GDK-Pixbuf for converting `.docx` to `.pdf`.  
> Make sure to install them using:
> ```bash
> brew install cairo pango gdk-pixbuf libffi  # macOS
> sudo apt install libcairo2 libpango-1.0-0 libgdk-pixbuf2.0-0 libffi-dev  # Debian/Ubuntu
> ```

---

## 🧪 How to Use

```bash
protocol-formatter path/to/input_protocol.txt
```

- You’ll be prompted to provide a path if not passed as argument.
- Output will be saved as a `.docx` file in the same folder.

---

## 📂 Input Format

Supports `.txt` files containing stepwise procedures like:

```
- Prepare solutions
* Mix reagents...
* Adjust pH...
** nested content

- Sample Treatment
* Add buffer
* Incubate at 37°C
```

---

## 🖨 Sample Output

A fully formatted DOCX output example:  
![Sample Output Preview](samples/sample_output.png)

---

## 🛠 Developer Notes

- Entry point defined in `__init__.py`
- Uses `python-docx` for Word file creation
- Compatible with Python 3.7+

---

## 📜 License

Licensed under the MIT License. See [`LICENSE`](LICENSE) for details.
