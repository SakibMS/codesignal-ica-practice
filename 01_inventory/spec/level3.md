# Level 3 — Reservations

Customers can now reserve units for a limited time.

- `reserve(timestamp, product_id, quantity, duration) -> str | None`
  Puts `quantity` units on hold. Held units leave the stock immediately, so `get_stock`, `sell`, `low_stock`, etc. no longer see them.
  - Returns a reservation id: `"res1"`, `"res2"`, ... numbered by the order of *successful* reservations across all products.
  - Returns `None` if the product doesn't exist or its stock is less than `quantity`.
  - The reservation expires at `timestamp + duration`. If it hasn't been confirmed by then, its units go back into stock at exactly that time.
- `confirm(timestamp, reservation_id) -> bool`
  Turns an active reservation into a sale (it now counts toward revenue). Returns `True` on success, or `False` if the reservation doesn't exist, was already confirmed, or has expired.

Notes:
- Expirations at time `t` happen before any other operation at time `t`. A reservation made at 3 with duration 10 can be confirmed at 12, but not at 13.
- Confirmed units never return to stock.

Run: `python3 run.py 1 --level 3`

### Example

```
add_product(1, "tv", 1000)
restock(2, "tv", 5)
reserve(3, "tv", 2, 10)        -> "res1"  # expires at 13
get_stock(4, "tv")             -> 3
confirm(5, "res1")             -> True    # tv revenue: 2000
reserve(6, "tv", 3, 10)        -> "res2"  # expires at 16
get_stock(7, "tv")             -> 0
get_stock(16, "tv")            -> 3       # res2 expired
confirm(17, "res2")            -> False
top_products(18, 1)            -> ["tv(2000)"]
```
