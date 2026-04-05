# Project Root Directory Structure

```text
pydbms/
├── .venv/                         (Virtual Environment - Content Skipped)
├── LICENSE                        (BSD-3-Clause License)
├── README.md                      (Project Documentation & System Evaluation)
├── architecture.md                (System Design & Architecture Blueprint)
├── changelog.md                   (Version History and Changes)
├── manifest.in                    (Packaging Rules)
├── patchnotes.md                  (Granular updates for recent versions)
├── pyproject.toml                 (PEP 518 Build System Config)
├── requirements.txt               (Project Dependencies)
├── pydbms/                        (Core Source Code)
│   ├── __init__.py
│   ├── db/                        (Database Connector Abstraction Layer)
│   │   ├── __init__.py
│   │   ├── db_base.py             (Base Interface for DB Connectors)
│   │   ├── db_errors.py           (DB Error Output Abstraction — DBErrorHandler + MySQLErrors)
│   │   ├── db_exceptions.py       (Custom Exception Classes for DB)
│   │   ├── db_manager.py          (Factory for initializing DB Drivers — uses pydbms_error())
│   │   └── mysql.py               (MySQL-specific Implementation — uses MySQLErrors)
│   ├── engine/                    (Cross-Engine Abstractions)
│   │   ├── __init__.py
│   │   └── engine_base.py         (ABC Base + Centralized pydbms_error/warning/info helpers)
│   ├── export/                    (Query Export Infrastructure)
│   │   ├── __init__.py
│   │   ├── export_base.py         (ABC Base Interface for Exporters — includes include_query)
│   │   ├── export_csv.py          (CSV Export — supports --include-query SQL embedding)
│   │   ├── export_json.py         (JSON Export — supports --include-query SQL embedding)
│   │   └── export_manager.py      (Resolver & Registrar for Export Formats)
│   ├── main/                      (CLI UX & Core Logic)
│   │   ├── __init__.py
│   │   ├── config.py              (Configuration loading & validation)
│   │   ├── core.py                (Application Entry Point & Main Loop — v4.1.0)
│   │   ├── dependencies.py        (Centralized External Imports, UI Components)
│   │   ├── meta_handler.py        (Dot-command `.help`, `.tables`, etc. — uses pydbms_error())
│   │   ├── profile.py             (Profile Dataclasses)
│   │   ├── pydbms_mysql.py        (MySQL Query Execution & Rendering — --row-limit support)
│   │   ├── pydbms_path.py         (Cross-platform Path Resolvers)
│   │   ├── query_parse_and_classify.py (SQL Parser — --expand, --export, --row-limit, --include-query)
│   │   └── runtime.py             (Global State / Printers)
│   └── profile/                   (User Authentication)
│       └── profile_auth.py        (Argon2 Hashing and Local Storage/Login Logic)
└── tests/                         (Automated Pytest Infrastructure)
    ├── __init__.py
    ├── test_config.py             (Validation Mapping Configs)
    ├── test_export_manager.py     (Path Constants, Format Checks, include_query tests)
    ├── test_pydbms_mysql.py       (Regex Pattern Matching Detectors)
    └── test_query_parse.py        (Shlex Query Flag Parsing — --row-limit, --include-query)
```
