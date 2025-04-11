# llmprint

**llmprint** is a CLI tool that prints directory structures and file contents in a clean, LLM-friendly format. It's perfect for generating context when pasting into a chatbot or code assistant.

---

## 🚀 Features

- 📂 Recursively includes multiple folders
- ✂️ Skips common clutter using `.gitignore`-style rules
- 🔍 Include/exclude specific folders and files
- 🧠 Great for LLM prompt preparation, code understanding, or debugging
- 📋 Cross-platform clipboard support
- 🌟 Clean, structured output format

---

## 📦 Installation

### Option 1: Install from source

```bash
git clone https://github.com/rsh3khar/llmprint.git
cd llmprint
pip install .
```

### Option 2: Install from pip

```bash
pip install llmprint
```

---

## ⚡️ Usage

### Print Directory Structure

```bash
# Print structure of current directory
llmprint -s

# Print structure of specific directories
llmprint -s -i src/ tests/
```

### Print File Contents Recursively

```bash
# Print contents of specific directories
llmprint -i src/ tests/

# Print all files in current directory
llmprint .
```

### Exclude Specific Folders or Files

```bash
# Exclude directories while printing contents
llmprint -i . -e node_modules __pycache__

# Exclude files by pattern (use quotes to prevent shell expansion)
llmprint -i . -e "*.pyc" "*.log"
```

### Copy to Clipboard

```bash
# Copy tree structure to clipboard
llmprint -s -c

# Copy file contents to clipboard
llmprint -i src/ -c

# Copy and also print to screen
llmprint -s -c -p
```

---

## 🧠 Why use this?

When prompting an LLM with questions like:
> "Can you explain this repo to me?"  
> "What's the purpose of this function?"  
> "Can you refactor this?"

You often need to include file structure and contents. `llmprint` formats this perfectly for large-context pasting — clean, readable, and structured.

---

## 🛠 Options

| Option              | Description                                           |
|--------------------|-------------------------------------------------------|
| `-s` / `--structure` | Print directory structure only                        |
| `-i` / `--include`   | Specify folders or files to include                   |
| `-e` / `--exclude`   | Specify folders or files to exclude (use quotes for patterns, e.g., "*.pyc") |
| `-c` / `--copy`      | Copy output to clipboard (suppresses stdout)          |
| `-p` / `--print`     | Print to stdout when using --copy                     |

If no flag is provided, it defaults to printing the directory structure.

---

## 🔧 Requirements

- Python 3.6 or higher
- `pyperclip` for clipboard operations

---

## 📄 License

[MIT License](LICENSE)

---

## ✨ Author

**Raj Shekhar**  
[GitHub: @rsh3khar](https://github.com/rsh3khar)
