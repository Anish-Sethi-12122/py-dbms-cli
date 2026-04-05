<div align="center">

  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:00ffff,100:8a2be2&height=200&section=header&text=PY%20DBMS&fontSize=80&fontAlign=50&fontAlignY=35&desc=Modern,%20Aesthetic%20and%20Secure%20DBMS%20Client&descAlign=50&descAlignY=55&animation=fadeIn&fontFace=Fira+Code" width="100%"/>

  [![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
  [![MySQL](https://img.shields.io/badge/MySQL-Supported-orange?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
  [![License](https://img.shields.io/badge/License-BSD_3_Clause-green?style=for-the-badge)](LICENSE)
  [![Status](https://img.shields.io/badge/Status-Experimental-success?style=for-the-badge)]()
  [![Version](https://img.shields.io/badge/Version-4.1.0-cyan?style=for-the-badge)]()

  <p align="center">
    <strong>A modern, secure, terminal-first MySQL client built for developers.</strong>
    <br />
    <em>Structured tables, smart flags, and secure local profiles—without the CLI clutter.</em>
  </p>

  <a href="#-introduction">Introduction</a> •
  <a href="#-key-features">Features</a> •
  <a href="#-installation">Installation</a> •
  <a href="#-usage-guide">Usage</a> •
  <a href="#-meta-flags--commands">Flags & Commands</a> •
  <a href="#-roadmap">Roadmap</a>
</div>

---

## ⚡ Introduction

**PY DBMS** is a UI/UX-focused **MySQL CLI client** built in Python. It replaces the traditional, low-signal database output with a high-fidelity terminal experience.

v4.0.0 overhauled the system completely to introduce **Secure Local Authentication**, **Live Query Spinners**, a hardened **Export Pipeline**, and intelligent multi-line prompt formatting (e.g. `    -> `). v4.1.0 stabilizes this architecture and brings powerful tools like inline `--row-limit` execution and `--include-query` export embedding.

> **The Philosophy:** Stop squinting at wrapped CLI output. Work in a visually structured, highly reliable environment that respects your time and your eyeballs.

---

## ✨ Why `pydbms`?

* **🚫 No More Walls of Text:** Utilizes `rich` to render data in clean, color-coded grid tables that respect your terminal bounds.
* **🔒 Authentication Guard:** Your database credentials shouldn't be unprotected. `pydbms` requires a local profile login verified by an `argon2` hashed password.
* **📊 One-Flag Exports:** Append `--export json` or `--export csv` to any query. No weird `INTO OUTFILE` permission issues from the backend server.
* **👀 Responsive UI:** See exactly what's happening. Executing a heavy `JOIN`? A cyan spinner keeps you updated. Broke a query? Explicit red `mysql error>` tags will let you know instantly.

---

## 🚀 Key Features

### 🎨 Terminal UI / UX
* **Live Query Spinners:** Long-running queries use an animated `Executing query...` spinner that clearly indicates network IO and properly vanishes before visualizing your result sets.
* **Structured Data Grids:** Results print into beautiful bordered panels with explicit column widths.
* **SQL Multi-Line Formatting:** Typing extensive queries prompts you with the MySQL-standard `    -> ` prefix across lines until terminated with `;`.

### 🛡️ Security & Authentication
* **Local Profiles Gate:** The CLI refuses to spin up a MySQL connection layer without validating against your local profile block.
* **Hardware-Grade Cryptography:** Local passwords are hashed via the `argon2-cffi` protocol. `profile.json` will never host plaintext payloads.
* **Masked Login Pipelines:** Password inputs globally obscure keystrokes using `pwinput`.

### 📤 Pluggable Export Engine
* **Non-Fatal Fallbacks:** Misspelled an export format? Missing disk write permissions? The export manager will catch the fault and warn you natively without blowing up your active session.
* **JSON & CSV Formats:** Built-in modular exporters ensure massive result rows are serialized efficiently.
* **Auto-Resolution Paths:** Output locations gracefully scale using `shlex` path parsing to support spaces (`export csv "C:\My Data\data.csv"`).

### ⚙️ Stateful Configurations
* **`config.json`:** Set global persistent states (like `export.path`) mapping directly to cross-session behaviors.
* **`.session-config`:** Temporarily mutate CLI states (like global expansions) strictly bounded by termination closures.

---

## 📦 Installation

### Prerequisites
* **Python 3.10+**
>Preferred latest Python version. Download from [Python's official website↗](https://www.python.org)
* A running **MySQL server**
>Download from [mysql's official website↗](https://www.mysql.com/)

### Quick Install via pip
```bash
pip install -U py-dbms-cli
```
>*(This automatically bootstraps all terminal dependencies identically into your virtual or global environment).*

### If installing via pipx
```bash
pipx install -U py-dbms-cli
```

---

# 🎮 Usage Guide

## 1. Launch the Shell
Open your terminal and boot up the client:
```bash
pydbms
```

## 2. Authentication Gate & Dashboard
On initial startup, `pydbms` will ask you to bootstrap your first local root user. Following startups will route through a standard login wall.  

<img src="https://github.com/Anish-Sethi-12122/py-dbms-cli/blob/main/pydbms%20banner.jpeg" alt="Dashboard Login">

## 3. Connect to MySQL Node
Post-authorization, your credentials for the target MySQL server are collected (with encrypted masking on your password).   `pydbms` will connect you to SQL server.

## 4. You're In !!
Once you are logged in to your SQL connection, everything operates within standard MySQL standard dialects. Queries process *exactly once* preventing accidental duplicate state mutation, returning cleanly visually bounded outputs.

Example usage:
```sql
pydbms> SELECT * FROM users
    -> WHERE access_tier = "admin"
    -> ORDER BY created_at DESC;
```

<img src="https://raw.githubusercontent.com/Anish-Sethi-12122/py-dbms-cli/main/example-usage-2-image" alt="Clean Result Rendering">

### Beautiful Error Catching
Mistakes happen. Instead of dumping a giant Python stack trace or messy string blocks on fail, exceptions are handled and printed uniformly for immediate bug patching.

<img src="https://raw.githubusercontent.com/Anish-Sethi-12122/py-dbms-cli/main/example-usage-1-image" alt="Beautiful Error Handling" width="800">

---

# 🕹 Meta Flags & Commands

### ⚡ Meta Flags (Query Overrides)
Flags are **appended explicitly to the end of standard SQL** queries, shifting display settings for a single action cycle without altering your base configurations. 

> **Usage Example:** `SELECT * FROM inventory; --expand --export csv`

| Flag | Description |
|------|-----------|
| `--expand` | Forces the output table to horizontally scroll over wrapping, preventing truncated columns at Terminal Edge boundaries. default=false|
| `--export <format> <path?>` | Rents out the result stack instantly to a local file in either `json` or `csv`. |
| `--row-limit <N>` | Limit rows returned for this query (overrides `ui.max_rows`). |
| `--include-query` | Embed original SQL query in the exported file (default: off). |

<br/>

### 🛠️ Meta Commands (Dot Commands)
Meta commands bypass the SQL parser outright to configure environments internally.

| Command | Description |
|------|-----------|
| `.help` | Show helper commands |
| `.databases` | Show databases in current connection |
| `.tables` | Show tables in current database |
| `.schema <table>` | Show CREATE TABLE statement for table `<table>` |
| `.clear` | Clear the terminal screen |
| `.version` | Show pydbms build information |
| `.config` | Show config settings for pydbms |
| `.config set <section>.<key> <value>` | Set config to a new value |
| `.config reset <section?>.<key?>` | Reset config to a default value |
| `.session-config` | Show session config settings for pydbms (Resets on every run) |
| `.session-config set <key> <value>` | Set session config to a new value |
| `.session-config reset <key?>` | Reset session config to a default value |
| `.exit` | Exit pydbms |

---

# ⚙️ Configuration Architecture

PY DBMS uses a highly flexible, **3-tiered configuration system**:

### 1. Global / Persistent (`config.json`)
Managed via `.config` set of commands. These configurations persist permanently across boots and are stored directly in your OS-appropriate `appdata`/`config` directory. 

### 2. Session / Ephemeral (`.session-config`)
Managed via `.session-config` and `.session-config set` commands. These overrides live **only in memory** for your current active terminal session and revert immediately when you exit via `.exit`.

### 3. Query-Level Overrides (Meta Flags)
Managed via appending raw `--flags` to the end of a SQL string. Overrides everything beneath it (Session and Global) for that **exact execution cycle only**.
- **Use Case:** Normal queries are truncating strings, but you just need to `SELECT` a massive JSON blob *once*? Do `SELECT * FROM logs; --expand`. It expands the blob, and the very next query goes back to normal.

---

```md
## 👤 Who is this for? Who can use `pydbms`

• Developers who prefer working in the terminal  
• Engineers who want cleaner query outputs  
• Users who frequently export query results  
• Anyone who wants a modern, secure, terminal-first MySQL client
• Students who are learning about databases and want a user-friendly way to interact with them

```

---

# 🗺 Roadmap  

* **Multi DBMS Support:** Built-in interactive command (`.use <db_name>`) for jumping database grids securely. *(Planned v5.x)*
* **Hardware Connectors:** Bridge the core codebase abstraction layer to support commonly used databases like Postgre, Mongo, Oracle SQL, etc.

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

# 👨‍💻 Author

<pre><i> <a href="https://www.linkedin.com/in/anish-sethi-dtu-cse/">Anish Sethi</a>      |      B.Tech Computer Science & Engineering      |      Delhi Technological University (Class of 2029)</i></pre>

---

## 📄 License
This project is licensed under the **BSD 3-Clause License**. See the [LICENSE](https://github.com/Anish-Sethi-12122/py-dbms-cli/blob/main/LICENSE).

<div align="center">
  <b>Hey! to the user of this project. Liked using pydbms ? <br>Consider dropping a ⭐️ star to support a student-led open-source project and keep the updates rolling in!</b>
</div>
