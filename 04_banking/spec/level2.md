# Level 2 — Top spenders

Add this method to `Bank`:

- `top_spenders(timestamp, n) -> list[str]`
  Returns the top `n` accounts by total outgoing money: the sum of all successful withdrawals and outgoing transfers.
  - Format each item as `"<account_id>(<total_outgoing>)"`.
  - Sort by total outgoing (descending), then by `account_id` (ascending, compared as strings).
  - Accounts with nothing outgoing are included with 0. If there are fewer than `n` accounts, return all of them.

Run: `python3 run.py 4 --level 2` (runs levels 1–2)

### Example

```
create_account(1, "alice")
create_account(2, "bob")
create_account(3, "carol")
deposit(4, "alice", 500)
deposit(5, "bob", 500)
transfer(6, "alice", "carol", 200)  -> 300
withdraw(7, "bob", 200)             -> 300
withdraw(8, "carol", 500)           -> None
top_spenders(9, 3)                  -> ["alice(200)", "bob(200)", "carol(0)"]
```
