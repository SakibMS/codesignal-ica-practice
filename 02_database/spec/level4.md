# Level 4 — Backup and restore

- `backup(timestamp) -> int`
  Saves a snapshot of the whole database. Returns the number of records that exist at that moment (records with at least one non-expired field).
- `restore(timestamp, timestamp_to_restore) -> bool`
  Replaces the entire database with the **latest backup taken at or before `timestamp_to_restore`**. Returns `True`, or `False` (and changes nothing) if there is no such backup.

TTL rules:
- A backup stores each field's *remaining* lifetime, not its absolute expiry time. Fields that have already expired are not saved.
- When restored at time `timestamp`, a field that had `r` left at backup time now expires at `timestamp + r`. Fields without a TTL stay permanent.
- Restoring doesn't remove any backups; the same backup can be restored again later.

Run: `python3 run.py 2 --level 4`

### Example

```
set_with_ttl(1, "s", "token", "abc", 10)   # expires at 11
set(2, "s", "user", "ann")
backup(5)                      -> 1       # token has 6 left
set(6, "s", "user", "bob")
restore(20, 5)                 -> True    # token now expires at 26
get(21, "s", "user")           -> "ann"
get_ttl(22, "s", "token")      -> 4
restore(23, 4)                 -> False   # no backup at or before 4
```
