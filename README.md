<div align="center">
  <h1>🐍 PY DBMS</h1>
  <p><strong>A Modern, Secure, and Blazing Fast MySQL CLI Client for Python</strong></p>

  <p>
    <a href="https://pypi.org/project/py-dbms-cli/"><img src="https://img.shields.io/pypi/v/py-dbms-cli?color=blue&style=for-the-badge" alt="PyPI version" /></a>
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.10+-blue.svg?style=for-the-badge" alt="Python 3.10+" /></a>
    <a href="https://opensource.org/licenses/BSD-3-Clause"><img src="https://img.shields.io/badge/license-BSD--3--Clause-green.svg?style=for-the-badge" alt="License" /></a>
  </p>
</div>

---

**PY DBMS** is a modern, developer-focused command-line client constructed entirely in Python. It's built for developers who live in the terminal but want a more **structured, responsive, and secure experience** than the default MySQL CLI provides.

With built-in secure local user profiles, deep UX polish (think execution spinners and MySQL-like multi-line formatting), and a first-class data export system, PY DBMS stands on its own as a premium database interaction layer.

---

## ✨ Features

### 🛡️ Secure Local Profiles (`profile_auth.py`)
- **Startup Gate:** You must log in via a local profile before PY DBMS spins up a MySQL connection. 
- **Argon2 Hashed:** Your local password is never stored in plaintext (`profile.json` relies purely on Argon2 hashed payloads via the `crypto-functions` library).
- **Masked Prompts:** `pwinput` safely hides your credentials as you type.

### 🎨 Stunning Terminal UX
- **Live Query Spinners:** Executing a massive `JOIN`? A sleek `cyan` spinner ensures you know the query is actively running in the background.
- **MySQL-Style Query Loops:** Type complex multi-line queries with ease natively formatted with `    -> ` line breaks.
- **Color-Coded Statuses:** All terminal errors log instantly with explicit visual warnings like `pydbms warning>` or `mysql error>`.

### 📤 Native Query Exports
- Export to `.csv` or `.json` instantly by appending `--export <format>` to any query.
- Completely **crash-safe**: Unresolved paths or permission errors fall back to clear UI warnings without dropping your session.
- Handles massive exports securely.

### 🛠️ Tiered Configuration
- **Global Config (`config.json`):** Set persistent states mapped cleanly across sessions.
- **Session Config (`.session-config`):** Hot-swap settings that reset the moment you exit.
- **Query Overrides (`--expand`):** On-the-fly execution changes explicitly attached to a single inline SQL execution.

---

## 🚀 Installation

### Prerequisites
- Python **3.10+**
- A running MySQL Server

### Install via pip
```bash
pip install -U py-dbms-cli
```

---

## 💻 Quick Start

### 1. Launch the Environment
```bash
pydbms
```

### 2. Authentication
On first launch, you'll be prompted to create a secure, hashed local profile. Next time, just log in!

### 3. Database Connection
You'll instantly be prompted to input your target MySQL Host, Username, and Password. PY DBMS ensures nothing is logged unencrypted to your disk.

### 4. Write SQL
Write your standard SQL inside the shell:
```sql
pydbms> SELECT * FROM users
    -> WHERE id > 100
    -> LIMIT 50;
```

---

## 📖 Helper Meta Commands

PY DBMS includes an array of `.` prefixed meta-commands that vastly speed up the database inspection process.

| Command | Description |
|------|-----------|
| `.help` | Show all helper commands |
| `.databases` | List all databases |
| `.tables` | List tables in the current database |
| `.schema <table>` | Show the exact `CREATE TABLE` definition |
| `.clear` | Clear the terminal screen |
| `.version` | Show build and MySQL version information |
| `.config` | Show persistent UI/Export configurations |
| `.config set <section>.<key> <value>` | Update a config value globally |
| `.config reset <section>.<key>` | Reset a config value |
| `.session-config` | Show session-level settings |
| `.session-config set <key> <value>` | Update a temporary session setting |
| `.exit` | Safely terminate the CLI and MySQL connection |

---

## ⚙️ Query Flags

Attach these raw flags to the very end of any valid SQL query.

| Flag | Description |
|------|-----------|
| `--expand` | Render the result set expanded vertically to bypass hard window truncation overrides. |
| `--export <format> [path]` | Extract your query locally to `csv` or `json`. |
| `--row-limit <N>` | Limit rows returned for this query (overrides `ui.max_rows`). |
| `--include-query` | Embed original SQL query in the exported file (default: off). |

**Example:**
```sql
SELECT * FROM access_logs WHERE status=404; --row-limit 100 --export json --include-query
```

---

## 🧪 Developer Testing

PY DBMS strictly utilizes `pytest` to govern all underlying architecture (Query Execution, Parsing, CSV/JSON Export flows, and Configuration Schemas).

All test pipelines are publicly committed to GitHub to ensure community pull requests maintain absolute stability.

To contribute or run tests locally on your machine:

```bash
# 1. Install the CLI with developer testing dependencies attached
pip install -e .[dev]

# 2. Run the test suite natively
pytest tests/
```

---

## 👨‍💻 Author

**Anish Sethi**  
B.Tech Computer Science & Engineering  
Delhi Technological University (Class of 2029)  
[LinkedIn](https://www.linkedin.com/in/anish-sethi-dtu-cse/) | [GitHub](https://github.com/Anish-Sethi-12122)

---

## 📄 License
This project is officially licensed under the **BSD 3-Clause License**. See the `LICENSE` file for details or type `.version` in the terminal for further context.
