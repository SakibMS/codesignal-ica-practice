# Level 4 — File versions

Files can now be updated, and each file keeps its version history.

- `update_file(timestamp, name, size) -> int | None`
  Replaces the file's contents with new contents of `size`, creating a new version. Returns the new version number. Returns `None` (and changes nothing) if the file doesn't exist or the new size doesn't fit in the owner's capacity. (The old size is freed first, so only the difference matters: a user with 100 capacity can grow their only file from 50 to 100.)
- `get_version(timestamp, name) -> int | None`
  Returns the file's current version number, or `None` if it doesn't exist.
- `restore_version(timestamp, name, version) -> int | None`
  Makes the contents of an earlier `version` current again by creating a **new** version with that size. Returns the new version number. Returns `None` (and changes nothing) if the file doesn't exist, the version doesn't exist, or the restored size doesn't fit in the owner's capacity (same rule as `update_file`).

Rules:
- A new file (from `add_file`, `add_file_by`, or as the destination of `copy_file`) starts at version 1.
- Only the current version counts toward the owner's capacity. `get_file_size`, `find_files`, `total_size`, and `update_capacity` all use the current size.
- Deleting a file deletes its history. A file added later with the same name starts again at version 1.

Run: `python3 run.py 3 --level 4`

### Example

```
add_file(1, "/notes.txt", 10)            -> True    # version 1
update_file(2, "/notes.txt", 25)         -> 2
update_file(3, "/notes.txt", 40)         -> 3
restore_version(4, "/notes.txt", 1)      -> 4       # size 10 again
get_file_size(5, "/notes.txt")           -> 10
get_version(6, "/notes.txt")             -> 4
```
