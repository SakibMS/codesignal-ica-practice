# Level 2 — Rankings

Add these methods to `Payroll`:

- `top_workers(timestamp, team, n) -> list[str]`
  Returns the top `n` employees of `team` by worked time (completed sessions only).
  - Format each item as `"<employee_id>(<worked_time>)"`.
  - Sort by worked time (descending), then by `employee_id` (ascending).
  - Return `[]` if the team has no employees. If it has fewer than `n`, return all of them.
- `team_totals(timestamp) -> list[str]`
  Returns every team with the total worked time of all its employees (completed sessions only).
  - Format each item as `"<team>(<total>)"`.
  - Sort by total (descending), then by team name (ascending).

Run: `python3 run.py 5 --level 2` (runs levels 1–2)

### Example

```
add_employee(1, "ann", "eng", 10)
add_employee(2, "bob", "eng", 10)
add_employee(3, "cy", "ops", 10)
clock_in(4, "ann")
clock_out(9, "ann")                 -> 5
clock_in(10, "cy")
clock_out(20, "cy")                 -> 10
top_workers(21, "eng", 2)           -> ["ann(5)", "bob(0)"]
team_totals(22)                     -> ["ops(10)", "eng(5)"]
```
