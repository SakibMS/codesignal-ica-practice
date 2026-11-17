# Level 3 — Pay

- `set_rate(timestamp, employee_id, rate) -> bool`
  Changes the employee's rate, starting at `timestamp`. Returns `False` if the employee doesn't exist.
- `get_pay(timestamp, employee_id, start, end) -> int | None`
  Returns what the employee earned for work done in the time range `[start, end)` (start inclusive, end exclusive). Returns `None` if the employee doesn't exist.

Rules:
- Only completed sessions are paid. A session from `in` to `out` covers `[in, out)`. If it only partly overlaps `[start, end)`, only the overlapping part is paid.
- Each unit of time is paid at the rate in effect at that time. A rate change during a session splits it: clock in at 10, rate change at 15, clock out at 20 → 5 units at the old rate + 5 units at the new rate.

Run: `python3 run.py 5 --level 3`

### Example

```
add_employee(1, "ann", "eng", 10)
clock_in(10, "ann")
set_rate(15, "ann", 20)             -> True
clock_out(20, "ann")                -> 10
get_pay(21, "ann", 0, 21)           -> 150   # 5 x 10 + 5 x 20
get_pay(22, "ann", 12, 18)          -> 90    # 3 x 10 + 3 x 20
```
