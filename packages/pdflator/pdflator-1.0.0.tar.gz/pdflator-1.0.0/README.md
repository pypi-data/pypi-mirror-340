# PDFlator 📄🌍

<p align="center">
  <img src="./pdflator/static/logo.png" alt="PDFlator Logo" width="200"/>
</p>

PDFlator is an application designed to translate PDF files while preserving their original layout. **Crucially, the primary goal of this project is not just the translation functionality itself, but to serve as a practical demonstration of modular software design, SOLID principles, and common design patterns (like Factory). It aims to be extensible and maintainable.**

## ✨ Features

- **PDF Translation**: Translate text content of PDF files.
- **Layout Preservation**: Maintains the original layout, including text positioning.
- **Language Selection**: Choose source/target languages, with auto-detection for the source.
- **Multiple Translation Providers**: Supports Google Translate and LibreTranslate (configurable API endpoint). Easily extendable with new providers.
- **Language-Specific Handling**: Adapts text alignment and bounding box resizing based on language characteristics (e.g., LTR vs. RTL). Extendable with new languages.
- **Web Interface**: User-friendly interface built with Flask.
    - Dark Theme: Sleek dark theme with green accents.
    - Configuration Page: Adjust translation parameters like font size, scaling, and redaction color via the UI (saved to `.env`).
- **Command Line Interface (CLI)**: Translate files directly from the terminal.
- **Configuration via `.env`**: Manage settings like font size, scaling factor, redaction color, and the LibreTranslate API endpoint (using `LIBRE_TRANSLATE_API`).
- **Installable Package**: Install via pip for easy use.
- *(Coming Soon)* Translation History: View past translations.

## 🎯 Project Philosophy & Design

This project emphasizes:

-   **Modularity**: Components (languages, translators) are designed as independent modules.
-   **Extensibility**: Adding new languages or translation providers requires creating new classes that inherit from abstract base classes (`Language`, `Translator`) without modifying core logic.
-   **SOLID Principles**: Adherence to principles like Single Responsibility and Open/Closed.
-   **Design Patterns**: Utilizes patterns like the Factory Method (`LanguageFactory`, `TranslatorFactory`) for object creation.

It serves as an example of building a maintainable application where functionality can be added or changed with minimal impact on existing code.

## 🛠️ Technologies Used

- **Python**: Core language.
- **Flask**: Web framework.
- **PyMuPDF (fitz)**: PDF processing.
- **googletrans**: Google Translate API access (Note: can be unstable).
- **libretranslatepy**: LibreTranslate API access.
- **python-dotenv**: Environment variable management.
- **Bootstrap**: Frontend styling.
- **Setuptools**: Packaging.

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- Pip (Python package manager)
- Git (for cloning)

### Installation

#### Option 1: Install as a Python Package (Recommended)

```bash
# Install from PyPI (if published)
# pip install pdflator

# Or for isolated installation (if published)
# pipx install pdflator

# Currently, install from source or use development mode
pip install git+https://github.com/your-username/PDFlator.git # Replace with actual URL if public
```

#### Option 2: Clone and Install Locally (Development)

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/PDFlator.git # Replace with actual URL
    cd PDFlator
    ```
2.  **Create and activate a virtual environment** (Recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3.  **Install in development mode**:
    ```bash
    pip install -e .
    # Or use the script: ./install_dev.sh
    ```
4.  **Configure Environment (`.env`)**:
    Create a `.env` file in the project root (where `setup.py` is located) with the following content:
    ```env
    OUTPUT_FONT_SIZE=12
    WHITE_COLOR=(1,1,1)
    SCALING_FACTOR=0.75
    LIBRE_TRANSLATE_API=http://localhost:8000/
    ```
    - Set `LIBRE_TRANSLATE_API` to the full URL of your LibreTranslate instance (e.g., `http://127.0.0.1:5000/`).
    - Other values can be configured via the web UI's Configuration page.

5.  **Set up LibreTranslate (Optional)**:
    If using the LibreTranslate provider, ensure a LibreTranslate API server is running and accessible at the URL specified in `LIBRE_TRANSLATE_API`. See the [LibreTranslate repository](https://github.com/LibreTranslate/LibreTranslate).

## 📖 Usage

*(Ensure your virtual environment is activated if installed locally)*

### Command Line Interface

PDFlator provides a unified CLI:

#### Directly Translate a PDF

```bash
# Basic translation (uses defaults from .env and code)
pdflator translate -i input.pdf -o output.pdf

# Specify languages and translator
pdflator translate -i input.pdf -o output.pdf -il fr -ol en -t gtrans

# Use LibreTranslate
pdflator translate -i input.pdf -o output.pdf -t libre
```
*Parameters are detailed in `pdflator translate --help`*

#### Start the Web Interface

```bash
# Start with default settings (http://127.0.0.1:5000)
pdflator web

# Specify host and port
pdflator web --host 0.0.0.0 --port 8080

# Run in debug mode
pdflator web --debug
```
*Parameters are detailed in `pdflator web --help`*

#### Other Commands

```bash
# Get version information
pdflator --version

# Display help for all commands
pdflator --help
```

### Web Interface

1.  Run `pdflator web`.
2.  Open the provided URL (e.g., `http://127.0.0.1:5000`) in your browser.
3.  Upload a PDF.
4.  Select languages and provider.
5.  Click "Translate".
6.  Download the result.
7.  Visit the "Configuration" page to adjust settings.

## 📂 Directory Structure

```
PDFlator/ (Project Root)
├── pdflator/              # Main package source code
│   ├── __init__.py
│   ├── main.py            # CLI entry point logic
│   ├── web.py             # Flask web application logic
│   ├── translate_pdf.py   # Core PDF translation function
│   ├── languages/         # Language-specific modules (e.g., alignment)
│   │   ├── __init__.py
│   │   ├── language.py    # Abstract Base Class for Language
│   │   └── ... (english.py, arabic.py, etc.)
│   ├── static/            # Static web assets (CSS, JS, images)
│   │   ├── __init__.py
│   │   └── css/
│   │       └── style.css
│   ├── templates/         # HTML templates for Flask
│   │   ├── __init__.py
│   │   └── ... (index.html, result.html, etc.)
│   └── translation/       # Translation provider modules
│       ├── __init__.py
│       ├── translator.py  # Abstract Base Class for Translator
│       └── ... (google_translator.py, libretranslate_translator.py, etc.)
├── .env                   # Environment variables (API URL, config) - *Not in Git*
├── .gitignore
├── MANIFEST.in            # Specifies files to include in the package
├── README.md              # This file
├── install_dev.sh         # Helper script for development install
├── pyproject.toml         # Build system requirements & tool config (Black, isort)
├── requirements.txt       # List of dependencies (can be generated from setup.py)
├── setup.py               # Package build and installation script
└── venv/                  # Virtual environment directory - *Not in Git*
```

## 🤝 Contributing

Contributions focusing on improving modularity, adding well-designed features, or enhancing demonstrations of design principles are welcome! Please open an issue first to discuss changes.

## 📜 License

MIT License. See the LICENSE file (if included) or standard MIT terms.

## 🌟 Acknowledgments

- [LibreTranslate](https://github.com/LibreTranslate/LibreTranslate)
- [googletrans](https://github.com/ssut/py-googletrans)
- [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/)
- [Flask](https://flask.palletsprojects.com/)

---

Happy Translating & Coding! 🌍💻