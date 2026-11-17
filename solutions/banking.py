"""
Reference solution: Banking System.

Design notes
- accounts: id -> {"balance", "outgoing"}; payments: id -> {...}.
- Scheduled payments run lazily: `_process(timestamp)` is the first line of
  every public method, so payments due at time t run before anything else
  at time t. Due payments run sorted by (due time, creation order).
- history: id -> [(time, balance or None)], appended whenever an account is
  created, changes balance, or is merged away (None). A payment is recorded
  at its *due* time, not when it was processed. get_balance_at is then a
  binary search for the last entry at or before time_at.
"""
import bisect
from typing import List, Optional


class Bank:
    def __init__(self):
        self.accounts = {}  # account_id -> {"balance": int, "outgoing": int}
        self.history = {}   # account_id -> [(time, balance or None)]
        self.payments = {}  # payment_id -> {"owner", "amount", "due", "seq", "status"}
        self.payment_count = 0

    # ---------- helpers ----------

    def _record(self, account_id: str, time: int) -> None:
        account = self.accounts.get(account_id)
        balance = None if account is None else account["balance"]
        self.history.setdefault(account_id, []).append((time, balance))

    def _process(self, timestamp: int) -> None:
        due = [p for p in self.payments.values()
               if p["status"] == "PENDING" and p["due"] <= timestamp]
        for payment in sorted(due, key=lambda p: (p["due"], p["seq"])):
            account = self.accounts[payment["owner"]]
            if account["balance"] >= payment["amount"]:
                account["balance"] -= payment["amount"]
                account["outgoing"] += payment["amount"]
                payment["status"] = "COMPLETED"
                self._record(payment["owner"], payment["due"])
            else:
                payment["status"] = "FAILED"

    def _owned_payment(self, account_id: str, payment_id: str) -> Optional[dict]:
        payment = self.payments.get(payment_id)
        if payment is None or account_id not in self.accounts or payment["owner"] != account_id:
            return None
        return payment

    # ---------- level 1 ----------

    def create_account(self, timestamp: int, account_id: str) -> bool:
        self._process(timestamp)
        if account_id in self.accounts:
            return False
        self.accounts[account_id] = {"balance": 0, "outgoing": 0}
        self._record(account_id, timestamp)
        return True

    def deposit(self, timestamp: int, account_id: str, amount: int) -> Optional[int]:
        self._process(timestamp)
        account = self.accounts.get(account_id)
        if account is None:
            return None
        account["balance"] += amount
        self._record(account_id, timestamp)
        return account["balance"]

    def withdraw(self, timestamp: int, account_id: str, amount: int) -> Optional[int]:
        self._process(timestamp)
        account = self.accounts.get(account_id)
        if account is None or account["balance"] < amount:
            return None
        account["balance"] -= amount
        account["outgoing"] += amount
        self._record(account_id, timestamp)
        return account["balance"]

    def transfer(self, timestamp: int, source_id: str, target_id: str, amount: int) -> Optional[int]:
        self._process(timestamp)
        source = self.accounts.get(source_id)
        target = self.accounts.get(target_id)
        if source is None or target is None or source_id == target_id or source["balance"] < amount:
            return None
        source["balance"] -= amount
        source["outgoing"] += amount
        target["balance"] += amount
        self._record(source_id, timestamp)
        self._record(target_id, timestamp)
        return source["balance"]

    def get_balance(self, timestamp: int, account_id: str) -> Optional[int]:
        self._process(timestamp)
        account = self.accounts.get(account_id)
        return None if account is None else account["balance"]

    # ---------- level 2 ----------

    def top_spenders(self, timestamp: int, n: int) -> List[str]:
        self._process(timestamp)
        ranked = sorted(self.accounts.items(), key=lambda item: (-item[1]["outgoing"], item[0]))
        return [f"{account_id}({acc['outgoing']})" for account_id, acc in ranked[:n]]

    # ---------- level 3 ----------

    def schedule_payment(self, timestamp: int, account_id: str, amount: int, delay: int) -> Optional[str]:
        self._process(timestamp)
        if account_id not in self.accounts:
            return None
        self.payment_count += 1
        payment_id = f"payment{self.payment_count}"
        self.payments[payment_id] = {
            "owner": account_id,
            "amount": amount,
            "due": timestamp + delay,
            "seq": self.payment_count,
            "status": "PENDING",
        }
        return payment_id

    def cancel_payment(self, timestamp: int, account_id: str, payment_id: str) -> bool:
        self._process(timestamp)
        payment = self._owned_payment(account_id, payment_id)
        if payment is None or payment["status"] != "PENDING":
            return False
        payment["status"] = "CANCELED"
        return True

    def get_payment_status(self, timestamp: int, account_id: str, payment_id: str) -> Optional[str]:
        self._process(timestamp)
        payment = self._owned_payment(account_id, payment_id)
        return None if payment is None else payment["status"]

    # ---------- level 4 ----------

    def merge_accounts(self, timestamp: int, account_id_1: str, account_id_2: str) -> bool:
        self._process(timestamp)
        if (account_id_1 == account_id_2
                or account_id_1 not in self.accounts
                or account_id_2 not in self.accounts):
            return False
        target = self.accounts[account_id_1]
        merged = self.accounts.pop(account_id_2)
        target["balance"] += merged["balance"]
        target["outgoing"] += merged["outgoing"]
        for payment in self.payments.values():
            if payment["owner"] == account_id_2:
                payment["owner"] = account_id_1
        self._record(account_id_1, timestamp)
        self._record(account_id_2, timestamp)  # records None: no longer exists
        return True

    def get_balance_at(self, timestamp: int, account_id: str, time_at: int) -> Optional[int]:
        self._process(timestamp)
        entries = self.history.get(account_id, [])
        times = [time for time, _ in entries]
        index = bisect.bisect_right(times, time_at)
        return None if index == 0 else entries[index - 1][1]
