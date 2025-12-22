## v2.0 - Experimental Release

- **Accurate Query Execution Feedback**
  - Distinguishes between successful execution, warnings, and errors
  - Removes misleading “no flags” messages from v1.0
- **Centralized Runtime Directory**
  - All pydbms-generated files now live in a dedicated OS-specific `pydbms/` directory
  - Cleaner filesystem usage and future-proof persistence
- **Config System (v2 foundation)**
  - Introduces a persistent `config.json`
  - Enables user-controlled behavior such as banner visibility (introduced as a concept, not utilized in v2.0)

## v2.1.2 - Stable Release
> NOTE: v2.1.0 had a bug while uploading to PyPI, hence v2.1.2 has been taken for stable release.  

  **Complete JSON Configuration System**
  - Fully implemented persistent `config.json`, stored in the OS-appropriate `pydbms/` directory on first run.
  - Configuration now persists across sessions and restores automatically if missing or corrupted.
  - Introduced a structured, nested configuration layout for:
    - UI settings (e.g., banner visibility)
    - MySQL connection settings
  - Added interactive inspection of configuration via the `.config` meta-command.
  - Startup banner behavior is now fully controlled through configuration.

  **Interactive Configuration Management**
  - Added `.config set <section.key> <value>` for modifying configuration values at runtime.
  - Added `.config reset <section.key>` to restore individual settings to their default values.
  - Configuration changes are validated and written to disk immediately.
