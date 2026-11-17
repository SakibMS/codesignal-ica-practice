# Level 4 — Prices and revenue history

Prices can now change, and the shop wants revenue reports for time ranges.

- `set_price(timestamp, product_id, price) -> bool`
  Sets a new unit price from now on. Returns `False` if the product doesn't exist.
- `get_revenue(timestamp, product_id, start, end) -> int | None`
  Returns the product's revenue from sales made at times between `start` and `end`, inclusive. Returns `None` if the product doesn't exist.

Rules:
- A `sell` is charged at the price in effect at the time of the sale. Past sales keep their price.
- A reservation **locks in the price at the time it was made**. When confirmed, it's charged at that locked price, and the sale happens at the time of `confirm`.
- `top_products` still ranks by total revenue: the sum of every sale at the price it was actually charged.

Run: `python3 run.py 1 --level 4`

### Example

```
add_product(1, "gum", 100)
restock(2, "gum", 10)
reserve(3, "gum", 2, 100)      -> "res1"  # locked at 100 each
set_price(4, "gum", 150)       -> True
sell(5, "gum", 1)              -> 7       # 150 at time 5
confirm(6, "res1")             -> True    # 200 at time 6
get_revenue(7, "gum", 5, 5)    -> 150
get_revenue(8, "gum", 0, 10)   -> 350
```
