<div align="center">

  <div align="center"> <img src="https://capsule-render.vercel.app/api?type=waving&color=0:00ffff,100:8a2be2&height=200&section=header&text=PY%20DBMS&fontSize=80&fontAlign=50&fontAlignY=35&desc=The%20Modern,%20Secure,%20all-in-one%20DBMS%20Client&descAlign=50&descAlignY=55&animation=fadeIn&fontFace=Fira+Code" alt="PY DBMS Banner" width="100%"/> </div>
  
  [![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
  [![MySQL](https://img.shields.io/badge/MySQL-Connector-orange?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
  [![License](https://img.shields.io/badge/License-BSD_3_Clause-green?style=for-the-badge)](LICENSE)
  [![Status](https://img.shields.io/badge/Status-Stable-brightgreen?style=for-the-badge)]()
  [![Version](https://img.shields.io/badge/Version-1.0-cyan?style=for-the-badge)](https://github.com/Anish-Sethi-12122/py-dbms-cli)

  <p align="center">
    <strong>A robust, aesthetic, modern and secure Command Line Interface for all your databases needs.</strong>
  </p>
  
  <a href="#-features">Features</a> •
  <a href="#-installation">Installation</a> •
  <a href="#-usage">Usage</a> •
  <a href="#-roadmap">Roadmap</a> •
  <a href="#-license">License</a>

</div>

---

# ⚡ Introduction

**PY DBMS** is a Python-based database client designed for developers who love the terminal but hate the clutter. A modern, secure, light-weight and the all-in-one DB client. Built on top of `mysql.connector` and powered by the ultimate UI/UX library `rich`, made secure by `pwinput`, it transforms raw SQL data into beautiful, readable tables.  
PS this is better than your MySQL CLI ;)  

Whether you are managing backend logic, debugging queries, or just exploring schemas, PY DBMS offers a **secure environment** with password masking, and an **easy-to-use experience** helper meta-commands.

---

# 🚀 Features

## 🎨 Visual & UI
* **Rich Terminal Interface:** Utilizes the `rich` library for colorful, formatted output.
* **Typewriter Effects:** Smooth text rendering for a polished user experience.
* **ASCII Branding:** Custom `pyfiglet` banner and dynamic dashboards.
* **Tabular Data:** Clean grid layouts for SQL results using `tabulate`.
* **Secure Terminal:** `pwinput` for masking password input, and state of the art ~~`cryptography`~~ (shhhhhhh.. no spoilers).

## 🛠 Functional
* **Smart SQL Parsing:** Supports multi-line queries (reads until `;` is detected).
* **Meta Commands:** Built-in shortcuts (like `.tables`, `.schema`) to save you time, and helper functions (like `.help`, `.version`) to get started.
* **Execution Timer:** Detailed execution time for every query which produces an output for performance monitoring.
* **Robust Error Handling:** Catches MySQL errors gracefully without crashing the session.

### 🛡 Security
* **Masked Input:** Uses `pwinput` to hide credentials during connection.
* **Localhost Default:** optimized for local development environments.

---

# 📦 Installation

## Prerequisites
Ensure you have latest stable **Python** and a running instance of **MySQL Server** installed.

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
Enter prompts for host, username and password for connection to `mysql`.  
<i>**NOTE:** For security purpose, password entering is masked with *</i>

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
`py-dbms-cli` includes a set of "dot commands" (also referred to as <i>Meta Commands</i> or <i>Meta Helper Commands</i> or <i>Meta Commands</i>)  
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
