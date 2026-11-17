from typing import Optional


class Inventory:
    """
    Inventory manager for a small shop. The task is described in spec/level1.md.
    Add the methods for later levels as you unlock them.
    """

    def __init__(self):
        # TODO: set up your data structures
        pass

    def add_product(self, timestamp: int, product_id: str, price: int) -> bool:
        """
        Adds a new product with unit `price` and stock 0.

        :return: True if added, False if `product_id` already exists.
        """
        # TODO: implement this method
        return False

    def restock(self, timestamp: int, product_id: str, quantity: int) -> Optional[int]:
        """
        Adds `quantity` units to the product's stock.

        :return: the new stock, or None if the product doesn't exist.
        """
        # TODO: implement this method
        return None

    def sell(self, timestamp: int, product_id: str, quantity: int) -> Optional[int]:
        """
        Removes `quantity` units from the product's stock.

        :return: the remaining stock, or None (and no change) if the product
                 doesn't exist or has fewer than `quantity` units.
        """
        # TODO: implement this method
        return None

    def get_stock(self, timestamp: int, product_id: str) -> Optional[int]:
        """
        :return: the product's current stock, or None if it doesn't exist.
        """
        # TODO: implement this method
        return None
