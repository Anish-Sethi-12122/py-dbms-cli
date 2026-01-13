<div align="center">

  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:00ffff,100:8a2be2&height=200&section=header&text=PY%20DBMS&fontSize=80&fontAlign=50&fontAlignY=35&desc=Modern,%20Aestheric%20and%20Secure,%20DBMS%20Client&descAlign=50&descAlignY=55&animation=fadeIn&fontFace=Fira+Code" width="100%"/>

  [![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
  [![MySQL](https://img.shields.io/badge/MySQL-Supported-orange?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
  [![License](https://img.shields.io/badge/License-BSD_3_Clause-green?style=for-the-badge)](LICENSE)
  [![Status](https://img.shields.io/badge/Status-Stable-success?style=for-the-badge)]()
  [![Version](https://img.shields.io/badge/Version-3.1.0-cyan?style=for-the-badge)]()

  <p align="center">
    <strong>A modern, secure, terminal-first DBMS client built for developers.</strong>
  </p>

  <a href="#-introduction">Introduction</a> •
  <a href="#-features">Features</a> •
  <a href="#-installation">Installation</a> •
  <a href="#-usage">Usage</a> •
  <a href="#-flags--export">Flags</a> •
  <a href="#-roadmap">Roadmap</a> •
  <a href="#-license">License</a>

</div>

---

## ⚡ Introduction

**PY DBMS** is a modern, UI/UX-focused **MySQL CLI client** built in Python for developers who prefer the terminal—but hate the clutter.

It replaces the cluttered, low-signal MySQL CLI with:
- clean tabular output,
- composable query flags,
- safe export workflows,
- and a robust configuration system.

> PS, this better than MySQL CLI.

---

## 🚀 Features

### 🎨 Terminal UI / UX
- **Rich-powered Interface** — clean tables, panels, and color-coded feedback
- **Readable Query Results** — structured output instead of raw text dumps
- **Consistent Visual Language** — success, warnings, and errors are instantly recognizable
- **Startup Dashboard** — session summary on launch

---

### 🧠 Smart Query Handling
- **Multi-line SQL Support** — execute only after `;`
- **Accurate Execution Feedback** — timing, rows returned, warnings
- **Single-execution Guarantee** — no duplicate queries, even with flags

---

### 📊 Query Output Control
- **`--expand` flag**
  - Expands columns to avoid truncation
  - Overrides session defaults **only for that query**
- **Session-level defaults**
  - Configure once, override when needed
- **Composable behavior**
  - `--expand` and `--export` work together cleanly

---

### 📤 Query Export System (Stable)
- **Pluggable Export Manager**
- **Supported formats**
  - CSV
  - JSON
- **Predictable UX**
  - Default `exports/` directory if path is not provided.
  - Timestamped filenames
- **Quoted paths supported**
  - Spaces in file paths work correctly (as path parsing is implemented using `shlex` library).
- **Non-fatal by design**
  - Export errors give a graceful reason for error, and never crash the session

---

### ⚙️ Configuration System
- **Persistent config**
  - Stored safely in an OS-appropriate runtime directory
- **Session config**
  - Runtime overrides without touching disk
- **Query-level overrides**
  - Flags like `--expand` override the session-config value.

---

### 🔐 Security
- **Masked password input**: `pwinput`
- **Credential Security**: sensitive connection details (like password) saved as an `argon2` hash.
- **Local-first philosophy**: works good on virtual environments.

---

## 📦 Installation

### Prerequisites
- Python **3.10+**
- A running **MySQL server**

### Install via PyPI
```bash
pip install py-dbms-cli
```

This step also installs all dependencies**  

---

# 🎮 Usage

## 1. Run from your terminal
```bash
pydbms
```

Upon entering the above command, you will see the dashboard panel, which prompts to login using `mysql` credentials  
<img src="https://github.com/Anish-Sethi-12122/py-dbms-cli/blob/main/Dashboard-Login-Image" alt="Dashboard">

## 2. Enter credentials (same as MySQL instance)  
You’ll be greeted with an interactive dashboard prompting MySQL credentials.  
><i>**NOTE:** Password input is masked for security</i>

## 3. All set
You are all ready to start using. Enter SQL commands as usual (in `mysql` syntax).  

### Querying
You can write standard SQL queries. The tool supports multi-line queries too:  

<img src="https://github.com/Anish-Sethi-12122/py-dbms-cli/blob/main/example-usage-2-image" alt="example-usage-2">

### Error Handling 
Errors are printed in bold red colour for easier debugging:  

<img src="https://github.com/Anish-Sethi-12122/py-dbms-cli/blob/main/example-usage-1-image" alt="example-usage-1">

### 🕹 Meta Helper Commands
`py-dbms-cli` includes a set of "dot commands" (also referred to as <i>Meta Commands</i> or <i>Meta Helper Commands</i> or <i>Helper Commands</i>)  
to make usage easier and faster.  

### **NEW** 🚩 Meta Flags (Query Overrides)

Unlike Meta Commands, **Meta Flags** are appended directly to the end of your SQL queries. They allow you to override display settings or execution behavior for a single statement without changing your global configuration.

> **Usage Syntax:** `<query> --<flag>`

| Flag | Description |
|------|-----------|
| `--expand` | Expand the result of query to not truncate in-view at End Of Line |
| `--export` | Export result of a query to save it |

**Usage:**  
`.help` to view all commands, and then command-specific syntax to be followed

---

# 🗺 Roadmap
We are constantly evolving! Below are some planned features for in-future updates for `pydbms`:  
* **User Profile:** Implement JSON structured user-profiles, for a local PY DBMS account, which enables a user to access multiple DBMS with user specific preferences/themes/etc.
* **Multi-Engine Support:** Currently we support only `mysql`, but in future we plan to support multiple DBMS engines such as `oracle-db`, `mongo-db`, etc.
* **Consistent Formatting across all DBMS:** Consistent `rich` UI themes across all DBMS.
* **JSON Export:** Integration into the new pluggable export system.
* **UI Themes:** To utilize `rich` to make preset theme settings for `py-dbms`.

---

# 👨‍💻 Author
<pre><i> <a href="https://www.linkedin.com/in/anish-sethi-dtu-cse/">Anish Sethi</a>      |      B.Tech Computer Science & Engineering      |      Delhi Technological University (Class of 2029)</i></pre>

---

## 📄 License
This project is licensed under the BSD 3-Clause License.

See the <a href="https://github.com/Anish-Sethi-12122/py-dbms-cli/blob/main/LICENSE">LICENSE</a> file for more details.
