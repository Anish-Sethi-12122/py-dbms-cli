<div align="center">

  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:00ffff,100:8a2be2&height=200&section=header&text=PY%20DBMS&fontSize=80&fontAlign=50&fontAlignY=35&desc=The%20Modern,%20Secure,%20all-in-one%20DBMS%20Client&descAlign=50&descAlignY=55&animation=fadeIn" alt="PY DBMS Banner" width="100%"/>

  [![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
  [![MySQL](https://img.shields.io/badge/MySQL-Connector-orange?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
  [![License](https://img.shields.io/badge/License-GPLv3-green?style=for-the-badge)](LICENSE)
  [![Status](https://img.shields.io/badge/Status-Stable-brightgreen?style=for-the-badge)]()
  [![Version](https://img.shields.io/badge/Version-1.0-cyan?style=for-the-badge&labelColor=000000&logo=verizon&logoColor=cyan)](https://github.com/Anish-Sethi-12122/py-dbms-cli/releases)

  <p align="center">
    <strong>A robust, aesthetic, and secure Command Line Interface for all your databases needs.</strong>
  </p>
  
  <a href="#-features">Features</a> •
  <a href="#-installation">Installation</a> •
  <a href="#-usage">Usage</a> •
  <a href="#-roadmap">Roadmap</a> •
  <a href="#-license">License</a>

</div>

---

## ⚡ Introduction

**PY DBMS** is a Python-based database client designed for developers who love the terminal but hate the clutter. A modern, secure, light-weight and the all-in-one DB client. Built on top of `mysql.connector` and powered by `rich`, it transforms raw SQL data into beautiful, readable tables. 

Whether you are managing backend logic, debugging queries, or just exploring schemas, PY DBMS offers a **secure environment** with password masking, syntax highlighting, and intuitive meta-commands.

---

## 🚀 Features

### 🎨 Visual & UI
* **Rich Terminal Interface:** Utilizes the `rich` library for colorful, formatted output.
* **Typewriter Effects:** Smooth text rendering for a polished user experience.
* **ASCII Branding:** Custom `pyfiglet` banners and dynamic dashboards.
* **Tabular Data:** Clean grid layouts for SQL results using `tabulate`.
* **Secure Terminal:** `cryptography` shhhhhhh.. no spoilers.

### 🛠 Functional
* **Smart SQL Parsing:** Supports multi-line queries (reads until `;` is detected).
* **Meta Commands:** Built-in shortcuts (like `.tables`, `.schema`) to save you time.
* **Execution Timer:** detailed execution time for every query for performance monitoring.
* **Robust Error Handling:** Catches MySQL errors gracefully without crashing the session.

### 🛡 Security
* **Masked Input:** Uses `pwinput` to hide credentials during connection.
* **Localhost Default:** optimized for local development environments.

---

## 📦 Installation

### Prerequisites
Ensure you have latest stable **Python** and a running instance of **MySQL Server** installed.

### 1. Clone the Repository
```bash
git clone [https://github.com/Anish-Sethi-12122/py-dbms-cli.git](https://github.com/Anish-Sethi-12122/py-dbms-cli.git)
cd py-dbms-cli```
