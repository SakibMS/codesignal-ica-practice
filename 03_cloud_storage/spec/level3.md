# Level 3 — Users and capacity

The service now has users, each with a storage capacity.

- `add_user(timestamp, user_id, capacity) -> bool`
  Adds a user who can own files with a total size of at most `capacity`. Returns `False` if the user already exists.
- `add_file_by(timestamp, user_id, name, size) -> int | None`
  Adds a file owned by `user_id` and returns the user's remaining capacity. Returns `None` (and adds nothing) if the user doesn't exist, the file already exists, or the file doesn't fit in the user's remaining capacity.
- `update_capacity(timestamp, user_id, capacity) -> int | None`
  Changes the user's capacity. If their files no longer fit, delete their largest files one at a time until they do (largest first; for equal sizes, the name that sorts first goes first). Returns how many files were deleted, or `None` if the user doesn't exist.

Rules:
- Files added with `add_file` belong to the built-in user `"admin"`, who has unlimited capacity. (Tests never pass `"admin"` to the methods above.)
- `copy_file`: the copy belongs to the source file's owner and uses their capacity. If it doesn't fit, `copy_file` returns `False`.
- `delete_file` frees the owner's capacity.

Run: `python3 run.py 3 --level 3`

### Example

```
add_user(1, "ann", 500)                  -> True
add_file_by(2, "ann", "/ann/a", 200)     -> 300
add_file_by(3, "ann", "/ann/b", 250)     -> 50
add_file_by(4, "ann", "/ann/c", 100)     -> None    # doesn't fit
copy_file(5, "/ann/a", "/ann/a2")        -> False   # copy needs 200 more
update_capacity(6, "ann", 300)           -> 1       # deletes /ann/b (largest)
add_file_by(7, "ann", "/ann/c", 100)     -> 0
```
