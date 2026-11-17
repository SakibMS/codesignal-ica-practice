# Payroll

Build a simplified time-tracking and payroll system. Implement the `Payroll` class in `payroll.py`.

The task has **4 levels**. Each level builds on the previous one, so finish a level before opening the next spec file.

**Rules for all levels**
- Every method's first argument is `timestamp` (int). Calls always arrive in strictly increasing `timestamp` order.
- Employee ids and team names are strings. Rates are positive integers (pay per unit of time).

Run this level's tests from the repo root: `python3 run.py 5 --level 1`

## Level 1 — Clocking in and out

- `add_employee(timestamp, employee_id, team, rate) -> bool`
  Adds an employee in `team` who earns `rate` per unit of time. Returns `False` if the id already exists.
- `clock_in(timestamp, employee_id) -> bool`
  Starts a work session. Returns `False` if the employee doesn't exist or is already clocked in.
- `clock_out(timestamp, employee_id) -> int | None`
  Ends the current session and returns its length (clock-out time minus clock-in time). Returns `None` if the employee doesn't exist or isn't clocked in.
- `get_worked_time(timestamp, employee_id) -> int | None`
  Returns the total length of the employee's **completed** sessions (an ongoing session doesn't count). Returns `None` if the employee doesn't exist.

### Example

```
add_employee(1, "ann", "eng", 10)   -> True
clock_in(2, "ann")                  -> True
clock_in(3, "ann")                  -> False   # already clocked in
clock_out(12, "ann")                -> 10
get_worked_time(13, "ann")          -> 10
clock_out(14, "ann")                -> None
```
