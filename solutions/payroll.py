"""
Reference solution: Payroll.

Design notes
- employees: id -> {"team", "rates": [(effective_from, rate)], "sessions": [(in, out)],
  "clocked_in_at"}. Keeping raw sessions (not just a running total) is what makes
  levels 3-4 possible.
- Pay is piecewise: the rate and the bonus multiplier only change at known points
  (rate changes, bonus period edges). `_pay` clips each session to [start, end),
  cuts it at those points, and sums length x rate x multiplier for each piece.
"""
from typing import List, Optional


class Payroll:
    def __init__(self):
        self.employees = {}  # employee_id -> dict (see notes above)
        self.bonuses = []    # [(start, end, multiplier)]

    # ---------- helpers ----------

    @staticmethod
    def _rate_at(employee: dict, time: int) -> int:
        rate = employee["rates"][0][1]
        for effective_from, new_rate in employee["rates"]:
            if effective_from > time:
                break
            rate = new_rate
        return rate

    def _multiplier_at(self, time: int) -> int:
        for start, end, multiplier in self.bonuses:
            if start <= time < end:
                return multiplier
        return 1

    def _pay(self, employee: dict, start: int, end: int) -> int:
        total = 0
        for session_in, session_out in employee["sessions"]:
            lo, hi = max(session_in, start), min(session_out, end)
            if lo >= hi:
                continue
            cuts = {lo, hi}
            cuts.update(t for t, _ in employee["rates"] if lo < t < hi)
            for bonus_start, bonus_end, _ in self.bonuses:
                cuts.update(t for t in (bonus_start, bonus_end) if lo < t < hi)
            points = sorted(cuts)
            for a, b in zip(points, points[1:]):
                total += (b - a) * self._rate_at(employee, a) * self._multiplier_at(a)
        return total

    # ---------- level 1 ----------

    def add_employee(self, timestamp: int, employee_id: str, team: str, rate: int) -> bool:
        if employee_id in self.employees:
            return False
        self.employees[employee_id] = {
            "team": team,
            "rates": [(timestamp, rate)],
            "sessions": [],
            "clocked_in_at": None,
        }
        return True

    def clock_in(self, timestamp: int, employee_id: str) -> bool:
        employee = self.employees.get(employee_id)
        if employee is None or employee["clocked_in_at"] is not None:
            return False
        employee["clocked_in_at"] = timestamp
        return True

    def clock_out(self, timestamp: int, employee_id: str) -> Optional[int]:
        employee = self.employees.get(employee_id)
        if employee is None or employee["clocked_in_at"] is None:
            return None
        started = employee["clocked_in_at"]
        employee["sessions"].append((started, timestamp))
        employee["clocked_in_at"] = None
        return timestamp - started

    def get_worked_time(self, timestamp: int, employee_id: str) -> Optional[int]:
        employee = self.employees.get(employee_id)
        if employee is None:
            return None
        return sum(out - start for start, out in employee["sessions"])

    # ---------- level 2 ----------

    def top_workers(self, timestamp: int, team: str, n: int) -> List[str]:
        ranked = sorted(
            (-self.get_worked_time(timestamp, eid), eid)
            for eid, employee in self.employees.items()
            if employee["team"] == team
        )
        return [f"{eid}({-neg_time})" for neg_time, eid in ranked[:n]]

    def team_totals(self, timestamp: int) -> List[str]:
        totals = {}
        for eid, employee in self.employees.items():
            team = employee["team"]
            totals[team] = totals.get(team, 0) + self.get_worked_time(timestamp, eid)
        ranked = sorted(totals.items(), key=lambda item: (-item[1], item[0]))
        return [f"{team}({total})" for team, total in ranked]

    # ---------- level 3 ----------

    def set_rate(self, timestamp: int, employee_id: str, rate: int) -> bool:
        employee = self.employees.get(employee_id)
        if employee is None:
            return False
        employee["rates"].append((timestamp, rate))
        return True

    def get_pay(self, timestamp: int, employee_id: str, start: int, end: int) -> Optional[int]:
        employee = self.employees.get(employee_id)
        if employee is None:
            return None
        return self._pay(employee, start, end)

    # ---------- level 4 ----------

    def add_bonus_period(self, timestamp: int, start: int, end: int, multiplier: int) -> bool:
        for other_start, other_end, _ in self.bonuses:
            if start < other_end and other_start < end:
                return False
        self.bonuses.append((start, end, multiplier))
        return True

    def top_earners(self, timestamp: int, n: int, start: int, end: int) -> List[str]:
        ranked = sorted(
            (-self._pay(employee, start, end), eid) for eid, employee in self.employees.items()
        )
        return [f"{eid}({-neg_pay})" for neg_pay, eid in ranked[:n]]
