"""
Reference solution: Inventory Manager.

Design notes
- One dict per entity type: products and reservations.
- Reservations expire lazily: `_expire(timestamp)` runs at the start of every
  public method, so expirations happen before anything else at that time.
- Each product keeps a sales log [(time, amount)], so total revenue (level 2)
  and revenue in a time range (level 4) are simple sums. A reservation stores
  the price it locked in when it was made.
"""
from typing import List, Optional


class Inventory:
    def __init__(self):
        # product_id -> {"price": int, "stock": int, "sales": [(time, amount)]}
        self.products = {}
        # reservation_id -> {"product_id", "quantity", "price", "expires_at", "status"}
        self.reservations = {}
        self.reservation_count = 0

    # ---------- helpers ----------

    def _expire(self, timestamp: int) -> None:
        for res in self.reservations.values():
            if res["status"] == "active" and res["expires_at"] <= timestamp:
                res["status"] = "expired"
                self.products[res["product_id"]]["stock"] += res["quantity"]

    @staticmethod
    def _revenue(product: dict) -> int:
        return sum(amount for _, amount in product["sales"])

    # ---------- level 1 ----------

    def add_product(self, timestamp: int, product_id: str, price: int) -> bool:
        self._expire(timestamp)
        if product_id in self.products:
            return False
        self.products[product_id] = {"price": price, "stock": 0, "sales": []}
        return True

    def restock(self, timestamp: int, product_id: str, quantity: int) -> Optional[int]:
        self._expire(timestamp)
        product = self.products.get(product_id)
        if product is None:
            return None
        product["stock"] += quantity
        return product["stock"]

    def sell(self, timestamp: int, product_id: str, quantity: int) -> Optional[int]:
        self._expire(timestamp)
        product = self.products.get(product_id)
        if product is None or product["stock"] < quantity:
            return None
        product["stock"] -= quantity
        product["sales"].append((timestamp, quantity * product["price"]))
        return product["stock"]

    def get_stock(self, timestamp: int, product_id: str) -> Optional[int]:
        self._expire(timestamp)
        product = self.products.get(product_id)
        return None if product is None else product["stock"]

    # ---------- level 2 ----------

    def top_products(self, timestamp: int, n: int) -> List[str]:
        self._expire(timestamp)
        ranked = sorted(
            ((self._revenue(p), pid) for pid, p in self.products.items()),
            key=lambda item: (-item[0], item[1]),
        )
        return [f"{pid}({revenue})" for revenue, pid in ranked[:n]]

    def low_stock(self, timestamp: int, threshold: int) -> List[str]:
        self._expire(timestamp)
        low = sorted(
            (p["stock"], pid) for pid, p in self.products.items() if p["stock"] < threshold
        )
        return [f"{pid}({stock})" for stock, pid in low]

    # ---------- level 3 ----------

    def reserve(self, timestamp: int, product_id: str, quantity: int, duration: int) -> Optional[str]:
        self._expire(timestamp)
        product = self.products.get(product_id)
        if product is None or product["stock"] < quantity:
            return None
        product["stock"] -= quantity
        self.reservation_count += 1
        reservation_id = f"res{self.reservation_count}"
        self.reservations[reservation_id] = {
            "product_id": product_id,
            "quantity": quantity,
            "price": product["price"],  # locked in now (matters in level 4)
            "expires_at": timestamp + duration,
            "status": "active",
        }
        return reservation_id

    def confirm(self, timestamp: int, reservation_id: str) -> bool:
        self._expire(timestamp)
        res = self.reservations.get(reservation_id)
        if res is None or res["status"] != "active":
            return False
        res["status"] = "confirmed"
        product = self.products[res["product_id"]]
        product["sales"].append((timestamp, res["quantity"] * res["price"]))
        return True

    # ---------- level 4 ----------

    def set_price(self, timestamp: int, product_id: str, price: int) -> bool:
        self._expire(timestamp)
        product = self.products.get(product_id)
        if product is None:
            return False
        product["price"] = price
        return True

    def get_revenue(self, timestamp: int, product_id: str, start: int, end: int) -> Optional[int]:
        self._expire(timestamp)
        product = self.products.get(product_id)
        if product is None:
            return None
        return sum(amount for time, amount in product["sales"] if start <= time <= end)
