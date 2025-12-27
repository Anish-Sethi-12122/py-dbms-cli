<div align="center">

  <div align="center">
    <img src="https://capsule-render.vercel.app/api?type=waving&color=0:00ffff,100:8a2be2&height=200&section=header&text=PY%20DBMS&fontSize=80&fontAlign=50&fontAlignY=35&desc=The%20Modern,%20Secure,%20all-in-one%20DBMS%20Client&descAlign=50&descAlignY=55&animation=fadeIn&fontFace=Fira+Code" alt="PY DBMS Banner" width="100%"/>
  </div>

  [![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
  [![MySQL](https://img.shields.io/badge/MySQL-Connector-orange?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
  [![License](https://img.shields.io/badge/License-BSD_3_Clause-green?style=for-the-badge)](LICENSE)
  [![Status](https://img.shields.io/badge/Status-Stable-brightgreen?style=for-the-badge)]()
  [![Version](https://img.shields.io/badge/Version-2.5.0-cyan?style=for-the-badge)](https://github.com/Anish-Sethi-12122/py-dbms-cli)

  <p align="center">
    <strong>A robust, aesthetic, modern, and secure Command Line Interface for database management.</strong>
  </p>

  <a href="#-whats-new-in-v250">What's New</a> •
  <a href="#-features">Features</a> •
  <a href="#-installation">Installation</a> •
  <a href="#-usage">Usage</a> •
  <a href="#-roadmap">Roadmap</a> •
  <a href="#-license">License</a>

</div>

---

# ⚡ Introduction

**PY DBMS** is a Python-based database client designed for developers who love the terminal but hate the clutter.

It is a **modern, secure, lightweight, all-in-one DBMS CLI** built on top of `mysql.connector`, powered by the `rich` UI library, and secured using `pwinput`.

It transforms raw SQL output into **clean, readable tables**, while providing a structured and predictable runtime experience.

> PS: Yes, this *is* better than the default MySQL CLI 😉

---

## ✨ What’s New in v2.5.0
> **v2.5.0** is a stable release built on the v2.x architecture, focused on configurability, UX clarity, and runtime control.

### 🔧 Session-Level Configuration (NEW)
A **non-persistent configuration layer** that allows runtime behavior changes without modifying `config.json`.

- Inspect active session settings using `.session-config`
- Modify session behavior using `.session-config set <key> <value>`
- Reset session settings using `.session-config reset <key>`
- Session configuration resets automatically on every new run

This ensures a **clean startup state** while enabling flexible experimentation.

---

### 🔍 Inline Query Output Control
- Added the `--expand` helper flag for **per-query column expansion**
- Designed to be explicit and non-invasive
- Does not mutate session or persistent configuration

---

### 🧭 Improved CLI Discoverability
- `.help` output now clearly separates:
  - Meta commands
  - Helper flags
- Refined help table layout for readability and future extensibility

---

### 🛡 Configuration Reliability Improvements
Strict separation between:
- Persistent configuration (`config.json`)
- Session-level configuration
- Query-level overrides

Includes hardened validation and automatic recovery from invalid or corrupted values.

---

### 🎨 UI & UX Refinements
- Unified visual theming across panels, tables, and help output
- Improved consistency while maintaining minimalism

---

# 🚀 Features

## 🎨 Visual & UI
- **Rich Terminal Interface:** Colorful, formatted output using `rich`
- **Clean Tables:** SQL results rendered in readable grid layouts
- **Unified Theming:** Consistent visuals across commands and output
- **Minimal & Focused UI:** Designed for long-running CLI sessions

## 🛠 Functional
- **Smart SQL Parsing:** Supports multi-line queries (terminated by `;`)
- **Meta Commands:** Built-in helpers like `.tables`, `.schema`, `.help`, `.version`
- **Query Semantics:** Execution status (success / warning / error) with timing
- **Robust Error Handling:** Graceful MySQL error handling without crashing sessions
- **Configuration Layers:**
  - Persistent (`config.json`)
  - Session-level (`.session-config`)
  - Query-level flags (`--expand`, etc.)

## 🛡 Security
- **Masked Input:** Passwords hidden using `pwinput`
- **Localhost-first:** Optimized for local development environments

---

# 📦 Installation

## Prerequisites
- Python **3.10+**
- A running **MySQL Server** instance

## Run the following command to download from pip
```
pip install py-dbms-cli
```

This step also installs all dependencies**  

---

# 🎮 Usage

## 1. Run from cmd
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

---

### Querying
You can write standard SQL queries. The tool supports multi-line input just like `mysql-cli`:  

<img src="https://github.com/Anish-Sethi-12122/py-dbms-cli/blob/main/example-usage-2-image" alt="example-usage-2">

### Error Handling 
Errors are printed in bold red colour for easier debugging:  

<img src="https://github.com/Anish-Sethi-12122/py-dbms-cli/blob/main/example-usage-1-image" alt="example-usage-1">

### 🕹 Meta Helper Commands
`py-dbms-cli` includes a set of "dot commands" (also referred to as <i>Meta Commands</i> or <i>Meta Helper Commands</i> or <i>Helper Commands</i>)  
to make usage easier and faster.

<img src="https://github.com/Anish-Sethi-12122/py-dbms-cli/blob/main/example-meta-image" alt="example-usage-1">

---

# 🗺 Roadmap
We are constantly evolving! Below are some planned features for in-future updates for `pydbms`:  
* **User Profile:** Implement JSON structured user-profiles, encrypted with python `cryptography` module.
* **Multi-Engine Support:** Currently we support only `mysql`, but in future we plan to support multiple DBMS engines such as `oracle-db`, `mongo-db`, etc.
* **Consistent Formatting across all DBMS:** Consistent `rich` UI themes across all DBMS.
* **Session History Export:** Exporting session history in structured JSON format.
* **UI Themes:** To utilize `rich` to make preset theme settings for `py-dbms`.

---

# 👨‍💻 Author
<pre><i> <a href="https://www.linkedin.com/in/anish-sethi-dtu-cse/">Anish Sethi</a>      |      B.Tech Computer Science & Engineering      |      Delhi Technological University (Class of 2029)</i></pre>

---

## 📄 License
This project is licensed under the BSD 3-Clause License.

See the <a href="https://github.com/Anish-Sethi-12122/py-dbms-cli/blob/main/LICENSE">LICENSE</a> file for more details.
