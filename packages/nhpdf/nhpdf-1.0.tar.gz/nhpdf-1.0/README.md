# NHENTAI DOUJIN-TO-PDF MAKER

A *disgusting* Python script that compiles doujins from [nhentai.net](https://nhentai.net) into PDFs for **offline gooning**.

This app has two flavors:

---

## 🧱 Flavor 1: CLI Tool (`nhpdf`)

A command-line interface you can run from anywhere:

```bash
nhpdf <doujin-code>
```

Example:
```bash
nhpdf 566212
nhpdf 566212 563102 345987
```

---

### 🔧 How to Install (CLI Version)

You can install the CLI tool in two ways:

#### Option 1: From PyPI

```bash
pip install nhpdf
```

#### Option 2: Locally (Development)

If you’ve cloned this repo:

```bash
cd NhentaiDoujinToPDFMaker
pip install .
```

Now you can run it with:

```bash
nhpdf 566212
```

---

## 🐍 Flavor 2: Raw Python Script (`main.py`)

If you prefer to run it like a normal Python script:

```bash
python main.py
# or
python3 main.py
```

---

### 📥 How to Set Up (Script Version)

> These instructions focus on **macOS**, but should work on **Windows** too (with small changes).

#### 1. Install Python

Search how to install Python for your OS.

Check if Python is installed:

- **Windows**:
  ```bash
  python
  ```

- **macOS**:
  ```bash
  python3
  ```

You should get a Python REPL (interactive shell).

---

#### 2. Install Required Packages

Navigate to the project directory (where `main.py` and `requirements.txt` live):

- **Windows**:
  ```bash
  cd path\to\your\folder
  dir  # list files
  ```

- **macOS/Linux**:
  ```bash
  cd /path/to/your/folder
  ls  # list files
  ```

Then install dependencies:

```bash
pip install -r requirements.txt
```

---

#### 3. Run the Script

```bash
python main.py
# or
python3 main.py
```

You should see:

```
NHENTAI DOUJIN-TO-PDF MAKER
```

✅ You’re good to go!

---

## 🧙 How to Use

Type the code of the nhentai doujin you want, then let the magic happen. The PDF will be saved to your **Documents/nhpdf/** folder.

---

> ⚠️ This script only works with [nhentai.net](https://nhentai.net)

---

## 🔗 Download

**GitHub Repo**: [NhentaiDoujinToPDFMaker](https://github.com/Aze543/NhentaiDoujinToPDFMaker)

You can download either version from the **[Releases](https://github.com/Aze543/NhentaiDoujinToPDFMaker/releases)** page.

---

Enjoy responsibly 😅
