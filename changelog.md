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

## v2.1.5 - Stable Release
> #NOTE: v2.1.0 had a bug while uploading to PyPI, hence version naming **v2.1.5** has been taken for stable release.    

  **Complete JSON Configuration System**
  - Fully implemented persistent `config.json`, stored in the OS-appropriate `pydbms/` directory on first run.
  - Configuration now persists across sessions and restores automatically if missing or corrupted.
  - Introduced a structured, nested configuration layout for:
    - UI settings (e.g., banner visibility)
    - MySQL connection settings
  - Added interactive inspection of configuration via the `.config` meta-command.
  - Startup banner behavior is now fully controlled through configuration.

  **Interactive Configuration Management**
  - Added `.config set <section>.<key> <value>` for modifying configuration values at runtime.
  - Added `.config reset <section>.<key>` to restore individual settings to their default values.
  - Configuration changes are validated and written to disk immediately.

## v2.5.0 – Stable Release
  **Session-Level Configuration System**
  - Introduced a non-persistent session configuration layer that allows runtime behavior changes without modifying `config.json`.
  - Added `.session-config` meta-command to inspect active session settings.
  - Added `.session-config set <key> <value>` for modifying session-only behavior.
  - Added `.session-config reset <key>` to restore individual session settings to defaults.
  - Session configuration resets automatically on every new run, ensuring a clean startup state.

  **Inline Query Output Control**
  - Added the `--expand` helper flag to allow per-query inline column expansion.
  - Designed to be non-invasive: does not mutate session or persistent configuration.

  **Improved CLI Discoverability**
  - Enhanced `.help` output with a dedicated **Helper Flags** section.
  - Flags and meta-commands are now clearly separated for improved readability and UX.
  - Help table layout refined for consistency and long-term extensibility.

  **Configuration Reliability Improvements**
  - Hardened configuration validation to safely recover from invalid or corrupted values.
  - Ensured strict separation between:
    - Persistent configuration (`config.json`)
    - Session-level configuration
    - Query-level overrides

  **UI & UX Refinements**
  - Unified visual theming across panels, tables, and help output for a consistent terminal experience.
  - Maintained minimalism while increasing discoverability of advanced features.
