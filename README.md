# Auto File Renamer

A lightweight desktop GUI tool for batch-renaming files in a selected folder.  
Built with Python and Tkinter — no third-party libraries required.

---

## Features

| Option | Description |
|--------|-------------|
| **Option 1** | Add rule text to the **front** of every file name |
| **Option 2** | Add rule text to the **back** of every file name (before the extension) |
| **Option 3** | Remove rule text from the **front** of every file name (skips files where the prefix is not found) |
| **Option 4** | Remove rule text from the **back** of every file name (skips files where the suffix is not found) |

- Browse to any folder with a single click
- Live log window shows every rename, skip, and failure in real time
- Summary pop-up after processing (Renamed / Skipped / Failed counts)

---

## Screenshots

> *(Add screenshots here)*

---

## Requirements

- Python 3.8 or later
- No third-party packages needed (`os` and `tkinter` are part of the Python standard library)

---

## Installation

```bash
git clone https://github.com/<your-username>/auto-file-renamer.git
cd auto-file-renamer
```

No `pip install` step is required.

---

## Usage

Run the script directly:

```bash
python "Auto file rename.py"
```

Or double-click the pre-built `Auto File Renamer.exe` (if available in the `dist/` folder).

### Steps

1. Click **Browse…** and select the folder that contains the files you want to rename.
2. Choose one of the four **Rename Options**.
3. Type the text you want to add or remove in the **File Name Rule** field.
4. Click **Apply Rename**.
5. Review the results in the **Log** window.

---

## Building an Executable (optional)

```bash
pip install pyinstaller
python -m PyInstaller --onefile --windowed --name "Auto File Renamer" "Auto file rename.py"
```

The `.exe` will be created in the `dist/` folder.

---

## License

MIT License — free to use and modify.
