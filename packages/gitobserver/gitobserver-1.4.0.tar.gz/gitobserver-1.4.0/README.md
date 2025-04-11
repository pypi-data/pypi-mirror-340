# 🧠 GitObserver – Intelligent Auto Commit Tool

GitObserver is an intelligent file monitoring and auto-committing tool for Git repositories. It watches your working directory for file changes and can commit them automatically or after confirmation. It’s perfect for developers who want real-time, stress-free version tracking while coding.

---

## 🚀 Features

- 🔄 **Automatic Git Commits**: Detects file changes and commits after a configurable delay.
- 🧠 **Pattern Mode**: Only commits on file modification events.
- 🕒 **Commit Timeout**: Prompts the user for confirmation; if no response within 2 minutes, commits automatically.
- 📑 **Change Summary**: Includes detailed commit messages listing added, modified, and deleted files.
- 🧰 **Lightweight & Customizable**: Easy CLI configuration with delay, message, and mode options.
- 🔒 **Hash-Based Change Detection**: Avoids false positives by verifying content changes via SHA-256 hash.
- 🛠️ **Modular Design**: Easy to extend with pluggable git and utility modules.

---

## 📂 Project Structure

```
git_observer/
│── git_observer/              # Source code directory
│   ├── __init__.py          # Initialization file
│   ├── git_handler.py       # Git commit handling module
│   ├── git_observer/        # File monitoring system
│   ├── main.py              # Main script
│
│── setup.py                 # Package configuration file
│── README.md                # Project documentation
│── LICENSE                  # Open-source license
│── requirements.txt          # Project dependencies
│── pyproject.toml            # (Optional, recommended for packaging)
│── tests/                    # Unit tests (Optional)
│
│── .gitignore                # Excludes unnecessary files
```

---

## 🔧 Installation

### 📥 Install from GitHub
```bash
git clone https://github.com/k2pme/gitobserver.git
cd gitobserver
pip install -r requirements.txt
```

### 📦 Install via pip
Once the package is published on PyPI:
```bash
pip install gitobserver
git_observer
```

---
## ✅ Available Options

| args       | description                            | deault         |
|:-----------|:--------------------------------------:|---------------:|
| --mode     | `auto` or `pattern`                    | auto           |
| --delay    | Time in seconds before auto-committing	| 30             |
| --message  | Default commit message	               | Auto update    |


### 📜 Commit Modes
- *Auto Mode* : Commits all detected changes after the delay.
- *Pattern Mode* : Commits immediately on file modification events only.



---

## 🧪 Usage
### 🛡️ Start Watching Your Folder

```bash
python3 -m git_observer.main --mode auto --delay 30 --message "Auto update"

```

### 📦 Example Commit Output

```bash
📝 Files to commit:
  - main.py
  - git_handler.py
⏳ Waiting for confirmation... (120s timeout)
```

---

## 👥 Contributors
- **k2pme** - [GitHub Profile](https://github.com/k2pme)

We welcome contributions from the community! 🚀

---

## 💡 How to Contribute
We appreciate your help in improving this project. Follow these steps to contribute:

1. **Fork the repository** on GitHub.
2. **Clone your fork**:
   ```bash
   git clone https://github.com/your-username/git-auto-commit.git
   ```
3. **Create a new branch** for your feature:
   ```bash
   git checkout -b feature-name
   ```
4. **Make your changes** and commit them:
   ```bash
   git commit -m "Added a new feature"
   ```
5. **Push to your fork**:
   ```bash
   git push origin feature-name
   ```
6. **Create a pull request** from your branch to the main repository.

---

## 🙏 Acknowledgments
Special thanks to all contributors and open-source maintainers who make projects like this possible.

If you find this project helpful, please ⭐ star the repository on GitHub!

---

### 📧 Contact
For any inquiries or feature requests, feel free to open an issue or contact us via GitHub.

🚀 Happy Coding!# gitobserver
