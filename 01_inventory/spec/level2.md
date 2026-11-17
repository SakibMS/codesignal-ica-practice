# Level 2 — Reports

Add these methods to `Inventory`:

- `top_products(timestamp, n) -> list[str]`
  Returns the top `n` products by total revenue. Revenue is the sum of `quantity × price` over all successful sales.
  - Format each item as `"<product_id>(<revenue>)"`.
  - Sort by revenue (descending), then by `product_id` (ascending) for ties.
  - Products with no sales have revenue 0 and are included. If there are fewer than `n` products, return all of them.
- `low_stock(timestamp, threshold) -> list[str]`
  Returns every product whose stock is strictly less than `threshold`.
  - Format each item as `"<product_id>(<stock>)"`.
  - Sort by stock (ascending), then by `product_id` (ascending).
  - Return `[]` if there are none.

Run: `python3 run.py 1 --level 2` (runs levels 1–2)

### Example

```
add_product(1, "a", 10)
add_product(2, "b", 5)
add_product(3, "c", 10)
restock(4, "a", 5)
restock(5, "b", 5)
restock(6, "c", 5)
sell(7, "a", 1)                -> 4       # a: revenue 10
sell(8, "b", 2)                -> 3       # b: revenue 10
top_products(9, 2)             -> ["a(10)", "b(10)"]
low_stock(10, 5)               -> ["b(3)", "a(4)"]
```
