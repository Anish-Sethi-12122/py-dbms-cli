<div align="center">

  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:00ffff,100:8a2be2&height=200&section=header&text=PY%20DBMS&fontSize=80&fontAlign=50&fontAlignY=35&desc=Modern,%20Aesthetic%20and%20Secure%20DBMS%20Client&descAlign=50&descAlignY=55&animation=fadeIn&fontFace=Fira+Code" width="100%"/>

  [![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
  [![MySQL](https://img.shields.io/badge/MySQL-Supported-orange?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
  [![License](https://img.shields.io/badge/License-BSD_3_Clause-green?style=for-the-badge)](LICENSE)
  [![Status](https://img.shields.io/badge/Status-Stable-success?style=for-the-badge)]()
  [![Version](https://img.shields.io/badge/Version-3.1.0-cyan?style=for-the-badge)]()

  <p align="center">
    <strong>A modern, secure, terminal-first DBMS client built for developers.</strong>
    <br />
    <em>Structured tables, smart flags, and seamless exports—without the CLI clutter.</em>
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

**PY DBMS** is a UI/UX-focused **MySQL CLI client** built in Python. It replaces the traditional, low-signal database output with a high-fidelity terminal experience. v3.1.0 introduces a stabilized, pluggable export system and hardened core execution for production-ready workflows.

> **The Philosophy:** Why work in a cluttered terminal when you can have a structured, aesthetic dashboard?

---

## ✨ Why pydbms?

* **🚫 No More Wall of Text:** Uses `Rich` to render data in clean, color-coded tables that actually fit your screen.
* **🔒 Security by Design:** Your DB passwords aren't sitting in a `.txt` file. We use `Argon2` hashing and credential masking.
* **📊 One-Flag Exporting:** Simply append `--export json` to any query. No more "SELECT INTO OUTFILE" headaches.
* **🧩 Built to Extend:** Completely refactored in v3.1.0 using OOP principles, making it easy to add your own Meta Flags.

---

## 🚀 Key Features

### 🎨 Terminal UI / UX
* **Rich-Powered Interface:** Clean tables, panels, and color-coded feedback (Success: Green, Error: Red, Warning: Yellow).
* **Startup Dashboard:** Automatic banner and helper table display on launch.
* **Readable Results:** Instead of raw text dumps, data is presented in structured tables using `rich.table`.

### 🧠 Smart Query Handling
* **Multi-line SQL:** Queries execute only after a semicolon `;` is detected.
* **Single-Execution Guarantee:** Even with multiple flags, your query runs exactly once to prevent accidental data mutation.
* **Accurate Feedback:** View execution timing, rows affected, and warnings in a dedicated panel.

### 📤 Stabilized Export System
* **JSON & CSV Support:** Choose your format on the fly.
* **Intelligent Pathing:** Support for quoted file paths with spaces (implemented via `shlex`).
* **Automated Filing:** Default `exports/` directory with deterministic, timestamped filenames, example:  
  `pydbms-export-root-2026-01-01_00-00-01.csv`
* **Non-Fatal Resilience:** Export errors provide graceful feedback without terminating your database session.

### ⚙️ Configuration & Security
* **Persistent Config:** Settings are saved across sessions in an OS-appropriate directory.
* **Credential Masking:** Password inputs are masked via `pwinput`.
* **Credential Hashing:** Sensitive connection details are stored using `argon2` hashes for local security.

---

## 📦 Installation

### Prerequisites
* **Python 3.10+**
* A running **MySQL server**

### Quick Install
```bash
pip install py-dbms-cli
```

This step also installs all dependencies**  

---

# 🎮 Usage

## 1. Launch the Client from your terminal
```bash
pydbms
```

Upon entering the above command, you will see the dashboard panel, which prompts to login using `mysql` credentials  
<img src="https://github.com/Anish-Sethi-12122/py-dbms-cli/blob/main/Dashboard-Login-Image.png" alt="Dashboard">

## 2. Enter credentials (same as MySQL instance)  
You’ll be greeted with an interactive dashboard prompting MySQL credentials.  
><i>**NOTE:** Password input is masked for security</i>

## 3. All set
You are all ready to start using. Enter SQL commands as usual (in `mysql` syntax).  

### Run Queries
You can use standard MySQL syntax. You can also append Meta Flags to override behavior.
```SQL
SELECT * FROM my_table
WHERE stock < 10;
--expand
```

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

| Flag | Syntax | Description |
|------|--------|-----------|
| `--expand` | `<query> --expand` | Expand the result of query to not truncate in-view at End Of Line |
| `--export` | `<query> --export <format> <path?>` | Export result of a query to save it |

**Usage:**  
`.help` to view all commands, and then command-specific syntax to be followed

---

# 🗺 Roadmap  

* **User Profiles:** Implement `pydbms` local profile system.
* **Multi-Engine:** Support for PostgreSQL, MongoDB, Oracle, etc.
* **UI Customization:** Customizable themes using rich color presets.
* **Query History:** Search and re-run previous queries across sessions.

---

# 👨‍💻 Author
<pre><i> <a href="https://www.linkedin.com/in/anish-sethi-dtu-cse/">Anish Sethi</a>      |      B.Tech Computer Science & Engineering      |      Delhi Technological University (Class of 2029)</i></pre>

---

## 📄 License
This project is licensed under the BSD 3-Clause License.

See the <a href="https://github.com/Anish-Sethi-12122/py-dbms-cli/blob/main/LICENSE">LICENSE</a> file for more details.

<div align="center"> Built with ❤️ for the developer community. </div>
