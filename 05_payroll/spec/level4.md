# Level 4 — Bonus periods

The company can now declare bonus periods (e.g. holidays) when pay is multiplied.

- `add_bonus_period(timestamp, start, end, multiplier) -> bool`
  Adds a bonus period `[start, end)`. Work during it is paid `multiplier` times the normal rate. Periods can be in the past or the future (they apply retroactively). Returns `False` (and adds nothing) if it overlaps an existing bonus period. Periods that only touch (one ends where the next starts) don't overlap.
- `top_earners(timestamp, n, start, end) -> list[str]`
  Returns the top `n` employees (all teams) by pay earned in `[start, end)`, using the same rules as `get_pay`.
  - Format each item as `"<employee_id>(<pay>)"`.
  - Sort by pay (descending), then by `employee_id` (ascending). Employees with 0 pay are included.

`get_pay` must take bonus periods into account too.

Run: `python3 run.py 5 --level 4`

### Example

```
add_employee(1, "ann", "eng", 10)
clock_in(10, "ann")
clock_out(30, "ann")                -> 20
add_bonus_period(31, 20, 40, 2)     -> True    # retroactive is fine
add_bonus_period(32, 0, 25, 3)      -> False   # overlaps [20, 40)
get_pay(33, "ann", 0, 40)           -> 300     # 10 x 10 + 10 x 10 x 2
top_earners(34, 1, 0, 40)           -> ["ann(300)"]
```
