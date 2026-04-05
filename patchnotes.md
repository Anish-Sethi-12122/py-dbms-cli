### Currently not working

* `--expand` meta flag not working
> Fixed

* `--export` meta flag saving exports to incorrect locations
> Fixed

* `--export` meta flag invalid syntax crashes the session
> Fixed

---

### To implement

* Add a support to export export all queries that return a result, currently only mysql valid queries are supported.
> Implemented

* Implement pydbms local account (`profile.json`). 
> Implemented

* Implement a new query level flag `--row-limit` to override persistent config setting for `ui.max_rows`.
> Implemented in stable v4.1.0

* Set a new query-level behaviour for exports to allow export to contain user query along with result table, provide an inline-flag to allow this. Usage as `<query>; --export <params?> --include-query`
> Implemented in stable v4.1.0

* Integrate `pytest` for automated unit testing (Config validation, Parser logic, Export handling).
> Implemented

* Maintain consistent UX across all files and all timelines.
> v4.1.0: Migrated all `Print("pydbms error/warning>")` to centralized helpers. Migrated all `Print("mysql error>")` to `MySQLErrors.error()` via new `db/db_errors.py` module. Fixed colour bug in `profile_auth.py`. Complete.

* Maintain modular code, preferably OOP (Object Oriented Programming) to make future extensions easier.
> v4.1.0: Introduced `DBErrorHandler` parent class + `MySQLErrors` subclass. ABC applied to export base. Full engine base integration deferred to v5.x series.

---

### Bugs

* Separate default folder path for export logic from default file path.
> Fixed

* `.config set/reset` on ui.max_rows is buggy.
> Fixed