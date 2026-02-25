# Project Root Directory Structure

```text
pydbms/
├── .venv/                         (Virtual Environment - Content Skipped)
├── LICENSE                        (BSD-3-Clause License)
├── README.md                      (Project Documentation & System Evaluation)
├── changelog.md                   (Version History and Changes)
├── manifest.in                    (Packaging Rules)
├── patchnotes.md                  (Granular updates for recent versons)
├── pyproject.toml                 (PEP 518 Build System Config)
├── requirements.txt               (Project Dependencies)
└── pydbms/                        (Core Source Code)
    ├── __init__.py
    ├── db/                        (Database Connector Abstraction Layer)
    │   ├── __init__.py
    │   ├── db_base.py             (Base Interface for DB Connectors)
    │   ├── db_exceptions.py       (Custom Exception Classes for DB)
    │   ├── db_manager.py          (Factory for initializing DB Drivers)
    │   └── mysql.py               (MySQL-specific Implementation of DBConnector)
    ├── export/                    (Query Export Infrastructure)
    │   ├── __init__.py
    │   ├── export_base.py         (Base Interface for Exporters)
    │   ├── export_csv.py          (CSV Export Logic)
    │   ├── export_json.py         (JSON Export Logic)
    │   └── export_manager.py      (Resolver & Registrar for Export Formats)
    ├── main/                      (CLI UX & Core Logic)
    │   ├── __init__.py
    │   ├── config.py              (Configuration loading & validation)
    │   ├── core.py                (Application Entry Point & Main Loop)
    │   ├── dependencies.py        (Centralized External Imports, UI Components)
    │   ├── meta_handler.py        (Dot-command `.help`, `.tables`, etc. Execution)
    │   ├── profile.py             (Profile Dataclasses)
    │   ├── pydbms_mysql.py        (MySQL specific Query Execution & Rendering)
    │   ├── pydbms_path.py         (Cross-platform Path Resolvers)
    │   ├── query_parse_and_classify.py (Custom SQL Parser with Flag parsing)
    │   └── runtime.py             (Global State / Printers)
    └── profile/                   (User Authentication)
            └── profile_auth.py        (Argon2 Hashing and Local Storage/Login Logic)
    ├── tests/                         (Automated Pytest Infrastructure)
    │   ├── __init__.py
    │   ├── test_config.py             (Validation Mapping Configs)
    │   ├── test_export_manager.py     (Path Constants & Format Checks)
    │   ├── test_pydbms_mysql.py       (Regex Pattern Matching Detectors)
    │   └── test_query_parse.py        (Shlex Query Flag Parsing System)
    ```
