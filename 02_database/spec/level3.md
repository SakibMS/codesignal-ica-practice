# Level 3 — Time to live (TTL)

Fields can now expire.

- `set_with_ttl(timestamp, key, field, value, ttl) -> None`
  Like `set`, but the field expires at `timestamp + ttl`. It is visible at times `t < timestamp + ttl` and gone from then on.
- `get_ttl(timestamp, key, field) -> int | None`
  Returns the field's remaining lifetime (`expiry - timestamp`), `-1` if the field never expires, or `None` if it doesn't exist.

Rules:
- Every earlier method must ignore expired fields. They behave exactly as if they had been deleted: `get` returns `None`, `delete` returns `False`, they're not in `scan` or `find`, and `delete_record` doesn't count them. A record whose fields have all expired doesn't exist.
- A plain `set` on an existing field removes its TTL (the new value never expires). `set_with_ttl` on an existing field replaces both its value and its expiry.

Run: `python3 run.py 2 --level 3`

### Example

```
set_with_ttl(1, "s", "token", "abc", 10)   # expires at 11
get_ttl(5, "s", "token")       -> 6
get(10, "s", "token")          -> "abc"
get(11, "s", "token")          -> None
set(12, "s", "user", "ann")
get_ttl(13, "s", "user")       -> -1
```
