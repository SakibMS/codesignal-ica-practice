# Level 3 — Scheduled payments

Accounts can now schedule payments for the future.

- `schedule_payment(timestamp, account_id, amount, delay) -> str | None`
  Schedules a payment of `amount` from the account, to run at `timestamp + delay` (`delay` is always > 0). Returns a payment id `"payment1"`, `"payment2"`, ... numbered by successful calls across all accounts, or `None` if the account doesn't exist.
- `cancel_payment(timestamp, account_id, payment_id) -> bool`
  Cancels a pending payment. Returns `False` if the payment doesn't exist, doesn't belong to `account_id`, or isn't pending anymore.
- `get_payment_status(timestamp, account_id, payment_id) -> str | None`
  Returns `"PENDING"`, `"COMPLETED"`, `"FAILED"`, or `"CANCELED"`. Returns `None` if the payment doesn't exist or doesn't belong to `account_id`.

How payments run:
- At its scheduled time, a payment withdraws `amount` if the balance is enough, and becomes `"COMPLETED"` (it counts as outgoing money for `top_spenders`). Otherwise nothing is withdrawn and it becomes `"FAILED"`.
- Payments due at time `t` run **before** any other operation at time `t`.
- Payments due at the same time run in the order they were scheduled.

Run: `python3 run.py 4 --level 3`

### Example

```
create_account(1, "alice")
deposit(2, "alice", 100)
schedule_payment(3, "alice", 60, 10)          -> "payment1"   # runs at 13
schedule_payment(4, "alice", 60, 10)          -> "payment2"   # runs at 14
cancel_payment(5, "alice", "payment2")        -> True
get_balance(13, "alice")                      -> 40
get_payment_status(14, "alice", "payment1")   -> "COMPLETED"
get_payment_status(15, "alice", "payment2")   -> "CANCELED"
```
