<div align="center">

  <div align="center">
    <img src="https://capsule-render.vercel.app/api?type=waving&color=0:00ffff,100:8a2be2&height=200&section=header&text=PY%20DBMS&fontSize=80&fontAlign=50&fontAlignY=35&desc=The%20Modern,%20Secure,%20all-in-one%20DBMS%20Client&descAlign=50&descAlignY=55&animation=fadeIn&fontFace=Fira+Code" alt="PY DBMS Banner" width="100%"/>
  </div>

  [![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
  [![MySQL](https://img.shields.io/badge/MySQL-Connector-orange?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
  [![License](https://img.shields.io/badge/License-BSD_3_Clause-green?style=for-the-badge)](LICENSE)
  [![Status](https://img.shields.io/badge/Status-Experimental-yellow?style=for-the-badge)]()
  [![Version](https://img.shields.io/badge/Version-3.0.0-cyan?style=for-the-badge)](https://github.com/Anish-Sethi-12122/py-dbms-cli)

  <p align="center">
    <strong>A robust, aesthetic, modern, and secure Command Line Interface for database management.</strong>
  </p>

  <a href="#-whats-new-in-v300">What's New</a> •
  <a href="#-features">Features</a> •
  <a href="#-installation">Installation</a> •
  <a href="#-usage">Usage</a> •
  <a href="#-roadmap">Roadmap</a> •
  <a href="#-license">License</a>

</div>

---

# ⚡ Introduction

**PY DBMS** is a Python-based database client designed for developers who love the terminal but hate the clutter.

It is a **modern, secure, lightweight, all-in-one DBMS CLI** built with a modular architecture. It transforms raw SQL output into **clean, readable tables** via the `rich` UI library, while ensuring security through masked `pwinput` prompts.

> PS: Yes, this *is* better than MySQL CLI 😉

---

## ✨ What’s New in v3.0.0
> **v3.0.0** is a major experimental release focusing on internal architecture modernization and long-term extensibility.

### 🏗️ Modular DB Connector Architecture (NEW)
We have decoupled the connection logic from the CLI core. This allows for:
- **Future Multi-Engine Support:** Ready-to-implement connectors for PostgreSQL, SQLite, etc.
- **Common Interface:** Standardized execution logic across different database types.

### 📤 Pluggable Query Export System
A new foundation for data portability:
- **Dedicated Export Manager:** Centralized handling of output formats.
- **CSV Support:** Initial implementation of direct-to-CSV exporting.
- **Non-Fatal Resilience:** Export failures or missing directories do not crash the active DB session.

### 🧱 Internal Result Abstraction
Introduced a structured result model that separates query execution from representation. This is the cornerstone for upcoming features like JSON exports and unified theming.

---

# 🚀 Features

## 🎨 Visual & UI
- **Rich Terminal Interface:** High-fidelity, colorful output using `rich`.
- **Clean Tables:** SQL results rendered in structured, readable grid layouts.
- **Typewriter Status:** Aesthetic, real-time status updates for a premium CLI feel.

## 🛠 Functional
- **Modular Design:** Built to scale beyond MySQL into a universal database tool.
- **Smart SQL Parsing:** Supports multi-line queries (terminated by `;`).
- **Meta Commands:** Dot-helpers like `.tables`, `.schema`, `.export <format>`, and `.config`.
- **Configuration Layers:** - **Persistent:** `config.json` for long-term preferences.
  - **Session-level:** `.session-config` for runtime experimentation.
  - **Query-level:** Inline flags like `--expand`.

## 🛡 Security
- **Masked Input:** Credentials are never echoed to the screen.
- **Zero-Persistence Policy:** Sensitive passwords are never saved in config files.

---

# 📦 Installation

## Prerequisites
- Python **3.10+**
- A running **MySQL Server** instance

## Run the following command in your terminal to download from PyPI:
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
