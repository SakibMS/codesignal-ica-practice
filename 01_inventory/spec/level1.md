# Inventory Manager

Build a simple inventory manager for a shop. Implement the `Inventory` class in `inventory.py`.

The task has **4 levels**. Each level builds on the previous one, so finish a level before opening the next spec file.

**Rules for all levels**
- Every method's first argument is `timestamp` (int). Calls always arrive in strictly increasing `timestamp` order.
- Ids are strings. Prices and quantities are positive integers.

Run this level's tests from the repo root: `python3 run.py 1 --level 1`

## Level 1 — Products and stock

- `add_product(timestamp, product_id, price) -> bool`
  Adds a new product with unit price `price` and stock 0. Returns `True` if it was added, or `False` if `product_id` already exists.
- `restock(timestamp, product_id, quantity) -> int | None`
  Adds `quantity` units to the product's stock. Returns the new stock, or `None` if the product doesn't exist.
- `sell(timestamp, product_id, quantity) -> int | None`
  Removes `quantity` units from stock and returns the remaining stock. Returns `None` (and changes nothing) if the product doesn't exist or has fewer than `quantity` units.
- `get_stock(timestamp, product_id) -> int | None`
  Returns the product's current stock, or `None` if it doesn't exist.

### Example

```
add_product(1, "apple", 50)    -> True
add_product(2, "apple", 70)    -> False   # already exists
restock(3, "apple", 10)        -> 10
sell(4, "apple", 4)            -> 6
sell(5, "apple", 7)            -> None    # only 6 left
get_stock(6, "apple")          -> 6
get_stock(7, "banana")         -> None
```
