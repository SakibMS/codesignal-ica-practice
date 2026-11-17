# Level 2 — Search

Add these methods to `CloudStorage`:

- `find_files(timestamp, prefix, suffix) -> list[str]`
  Returns files whose names start with `prefix` and end with `suffix` (an empty string matches anything).
  - Format each item as `"<name>(<size>)"`.
  - Sort by size (descending), then by name (ascending).
  - Return at most **10** results: the first 10 in that order.
- `total_size(timestamp, prefix) -> int`
  Returns the total size of all files whose names start with `prefix` (0 if there are none).

Run: `python3 run.py 3 --level 2` (runs levels 1–2)

### Example

```
add_file(1, "/img/a.png", 300)
add_file(2, "/img/b.png", 500)
add_file(3, "/img/c.jpg", 500)
add_file(4, "/docs/d.png", 100)
find_files(5, "/img/", ".png") -> ["/img/b.png(500)", "/img/a.png(300)"]
find_files(6, "/", "")         -> ["/img/b.png(500)", "/img/c.jpg(500)", "/img/a.png(300)", "/docs/d.png(100)"]
total_size(7, "/img/")         -> 1300
```
