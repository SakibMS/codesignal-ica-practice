# Level 2 — Scans and lookups

Add these methods to `Database`:

- `scan(timestamp, key, prefix) -> list[str]`
  Returns the fields of record `key` whose names start with `prefix` (an empty prefix matches every field).
  - Format each item as `"<field>(<value>)"`.
  - Sort by field name (ascending).
  - Return `[]` if the record doesn't exist or nothing matches.
- `find(timestamp, field, value) -> list[str]`
  Returns the keys of all records whose `field` equals `value`, sorted ascending. Return `[]` if there are none.

Run: `python3 run.py 2 --level 2` (runs levels 1–2)

### Example

```
set(1, "app", "db_port", "5432")
set(2, "app", "db_host", "local")
set(3, "app", "debug", "on")
set(4, "web", "debug", "on")
scan(5, "app", "db")           -> ["db_host(local)", "db_port(5432)"]
scan(6, "app", "")             -> ["db_host(local)", "db_port(5432)", "debug(on)"]
find(7, "debug", "on")         -> ["app", "web"]
```
