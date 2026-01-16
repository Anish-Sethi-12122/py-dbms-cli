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

---

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

---

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

---

## v3.0.0 - Experimental Release

**Database Connection Architecture (NEW)**
- Introduced a modular DB connector architecture to decouple connection logic from the CLI core.
- Added a common connector interface to enable future multi-engine support without refactoring core execution logic.
- MySQL support has been migrated to the new architecture with no change in user-facing behavior.

**Query Export System (v3 foundation)**
- Introduced a pluggable export system with a dedicated exporter interface.
- Added an export manager to centralize format handling and future extensibility.
- Implemented CSV export support using the new architecture.
- Export operations are non-fatal: invalid formats or misuse do not terminate the CLI session.

**Internal Result Abstraction**
- Added a structured query result model to clearly separate:
  - Query execution
  - Result representation
  - Output/export concerns
- This abstraction serves as the foundation for future export formats (JSON, etc.).

**UI Compatibility Guarantee**
- Preserved existing query UX and helper syntax to ensure backward compatibility during architectural migration.
- User-facing behavior remains familiar while internals evolve.

**Experimental Notes & Limitations**
- Export UX, default filenames, and additional formats are intentionally minimal in this release.
- Profile system integration and JSON export are deferred to **v3.1.0 (Stable)**.
- Internal APIs may change before stabilization.

---

## v3.1.0 — Stable Release

This release introduces major architectural changes and finalizes the architecture introduced in v3.0.0 and delivers a stable, fully composable query export and output-control system.

### Query Export System (Stabilized)
- Added **JSON export support** alongside CSV.
- Enforced strict export syntax:  
  `<query> --export <format> <path?>`
- Implemented predictable default export behavior:
  - Automatic `exports/` directory creation
  - Deterministic filenames with timestamps
- Added support for **quoted file paths with spaces** (implemented via `shlex`).
- Hardened error handling:
  - Invalid formats
  - Incorrect usage
  - Empty result sets
- Export failures never terminate the active session.

### Inline Output Control (`--expand`)
- Finalized `--expand` behavior with clear precedence rules:
  - Query-level `--expand` overrides session configuration
  - Session configuration defines default wrapping behavior
- Ensured `--expand` composes correctly with `--export`.
- Fixed rendering inconsistencies and eliminated duplicate query execution.
- Improved stability by resolving a function signature mismatch in overflow handling.

### Core Execution Reliability
- Guaranteed **single execution per query**, regardless of flag combinations.
- Improved control-flow structure for flag composition.
- Eliminated edge-case crashes related to configuration mapping.

### UX & CLI Consistency
- Standardized export-related success and error messages.
- Improved `.help` documentation for helper flags.
- Preserved backward compatibility with existing query syntax.

### Internal Quality Improvements
- Strengthened separation between:
  - Query execution
  - Result rendering
  - Export handling
- Reduced coupling between CLI control flow and rendering logic.
- Improved long-term maintainability and extensibility.
