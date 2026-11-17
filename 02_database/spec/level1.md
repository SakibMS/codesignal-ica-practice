# In-Memory Database

Build a simplified in-memory database. Each **record** is identified by a `key` and holds **fields** (field name → string value). Implement the `Database` class in `database.py`.

The task has **4 levels**. Each level builds on the previous one, so finish a level before opening the next spec file.

**Rules for all levels**
- Every method's first argument is `timestamp` (int). Calls always arrive in strictly increasing `timestamp` order.
- Keys, fields, and values are strings.

Run this level's tests from the repo root: `python3 run.py 2 --level 1`

## Level 1 — Records and fields

- `set(timestamp, key, field, value) -> None`
  Sets `field` of record `key` to `value`. Creates the record if needed and overwrites any existing value.
- `get(timestamp, key, field) -> str | None`
  Returns the field's value, or `None` if the record or field doesn't exist.
- `delete(timestamp, key, field) -> bool`
  Removes the field. Returns `True` if it existed, `False` otherwise. A record with no fields left no longer exists.
- `delete_record(timestamp, key) -> int`
  Removes the whole record. Returns how many fields it had (0 if the record doesn't exist).

### Example

```
set(1, "user1", "name", "Ada")
set(2, "user1", "city", "Paris")
get(3, "user1", "name")        -> "Ada"
get(4, "user1", "age")         -> None
delete(5, "user1", "city")     -> True
delete(6, "user1", "city")     -> False
delete_record(7, "user1")      -> 1
get(8, "user1", "name")        -> None
```
