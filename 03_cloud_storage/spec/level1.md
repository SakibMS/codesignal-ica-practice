# Cloud Storage

Build a simplified cloud file storage service. Implement the `CloudStorage` class in `cloud_storage.py`.

The task has **4 levels**. Each level builds on the previous one, so finish a level before opening the next spec file.

**Rules for all levels**
- Every method's first argument is `timestamp` (int). Calls always arrive in strictly increasing `timestamp` order.
- File names are strings like `"/docs/cv.pdf"`. They're just names; there are no real folders. Sizes are positive integers.

Run this level's tests from the repo root: `python3 run.py 3 --level 1`

## Level 1 — Files

- `add_file(timestamp, name, size) -> bool`
  Adds a new file. Returns `True`, or `False` if a file with that name already exists.
- `get_file_size(timestamp, name) -> int | None`
  Returns the file's size, or `None` if it doesn't exist.
- `delete_file(timestamp, name) -> int | None`
  Deletes the file and returns its size, or `None` if it doesn't exist.
- `copy_file(timestamp, source, dest) -> bool`
  Creates `dest` as a copy of `source` (same size). Returns `False` if `source` doesn't exist or `dest` already exists. The copy is independent of the original.

### Example

```
add_file(1, "/docs/cv.pdf", 200)                 -> True
add_file(2, "/docs/cv.pdf", 300)                 -> False
copy_file(3, "/docs/cv.pdf", "/backup/cv.pdf")   -> True
get_file_size(4, "/backup/cv.pdf")               -> 200
delete_file(5, "/docs/cv.pdf")                   -> 200
get_file_size(6, "/docs/cv.pdf")                 -> None
```
