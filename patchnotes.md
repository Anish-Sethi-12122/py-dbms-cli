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
> to implement in stable v4.1.0

* Set a new query-level default behaviour for exports to allow export to contain user query along with result table, provide an inline-flag to allow disable. Usage as `<query>; --export <params?> --include-query -n`
> to implement in stable v4.1.0

* Integrate `pytest` for automated unit testing (Config validation, Parser logic, Export handling).
> Implemented

---

### Bugs

* Separate default folder path for export logic from default file path.
> Fixed

* `.config set/reset` on ui.max_rows is buggy.
> Fixed
