# Banking System

Build a simplified banking system. Implement the `Bank` class in `banking.py`.

The task has **4 levels**. Each level builds on the previous one, so finish a level before opening the next spec file.

**Rules for all levels**
- Every method's first argument is `timestamp` (int). Calls always arrive in strictly increasing `timestamp` order.
- Account ids are strings. Amounts are positive integers.

Run this level's tests from the repo root: `python3 run.py 4 --level 1`

## Level 1 — Accounts

- `create_account(timestamp, account_id) -> bool`
  Creates an account with balance 0. Returns `False` if it already exists.
- `deposit(timestamp, account_id, amount) -> int | None`
  Adds money and returns the new balance, or `None` if the account doesn't exist.
- `withdraw(timestamp, account_id, amount) -> int | None`
  Removes money and returns the new balance. Returns `None` (and changes nothing) if the account doesn't exist or has insufficient funds.
- `transfer(timestamp, source_id, target_id, amount) -> int | None`
  Moves money from `source_id` to `target_id` and returns the source's new balance. Returns `None` (and changes nothing) if either account doesn't exist, they're the same account, or the source has insufficient funds.
- `get_balance(timestamp, account_id) -> int | None`
  Returns the balance, or `None` if the account doesn't exist.

### Example

```
create_account(1, "alice")          -> True
create_account(2, "alice")          -> False
create_account(3, "bob")            -> True
deposit(4, "alice", 500)            -> 500
withdraw(5, "alice", 600)           -> None
transfer(6, "alice", "bob", 200)    -> 300
get_balance(7, "bob")               -> 200
```
