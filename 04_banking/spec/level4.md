# Level 4 — Merges and balance history

- `merge_accounts(timestamp, account_id_1, account_id_2) -> bool`
  Merges account 2 into account 1, then deletes account 2. Returns `False` if the ids are equal or either account doesn't exist.
  - Account 1 gets account 2's balance and its total outgoing (for `top_spenders`).
  - All of account 2's payments (any status) now belong to account 1, keeping their ids and scheduled times.
  - Account 2 no longer exists. Its id can be used again by `create_account`, which creates a brand-new account.
- `get_balance_at(timestamp, account_id, time_at) -> int | None`
  Returns the balance `account_id` had at time `time_at` (`time_at <= timestamp`), after all operations at `time_at`. Returns `None` if the account didn't exist at `time_at` (not created yet, or already merged into another account).

Note: a scheduled payment changes the balance at its scheduled time, even if your code only processes it later.

Run: `python3 run.py 4 --level 4`

### Example

```
create_account(1, "alice")
create_account(2, "bob")
deposit(3, "alice", 100)
deposit(4, "bob", 50)
merge_accounts(5, "alice", "bob")   -> True
get_balance(6, "alice")             -> 150
get_balance(7, "bob")               -> None
get_balance_at(8, "alice", 4)       -> 100
get_balance_at(9, "bob", 4)         -> 50
get_balance_at(10, "bob", 5)        -> None
```
