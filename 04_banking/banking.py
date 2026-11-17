from typing import Optional


class Bank:
    """
    Banking system. The task is described in spec/level1.md.
    Add the methods for later levels as you unlock them.
    """

    def __init__(self):
        # TODO: set up your data structures
        pass

    def create_account(self, timestamp: int, account_id: str) -> bool:
        """
        Creates an account with balance 0.

        :return: True if created, False if it already exists.
        """
        # TODO: implement this method
        return False

    def deposit(self, timestamp: int, account_id: str, amount: int) -> Optional[int]:
        """
        :return: the new balance, or None if the account doesn't exist.
        """
        # TODO: implement this method
        return None

    def withdraw(self, timestamp: int, account_id: str, amount: int) -> Optional[int]:
        """
        :return: the new balance, or None (and no change) if the account
                 doesn't exist or has insufficient funds.
        """
        # TODO: implement this method
        return None

    def transfer(self, timestamp: int, source_id: str, target_id: str, amount: int) -> Optional[int]:
        """
        Moves `amount` from `source_id` to `target_id`.

        :return: the source's new balance, or None (and no change) if either
                 account doesn't exist, they're the same account, or the
                 source has insufficient funds.
        """
        # TODO: implement this method
        return None

    def get_balance(self, timestamp: int, account_id: str) -> Optional[int]:
        """
        :return: the balance, or None if the account doesn't exist.
        """
        # TODO: implement this method
        return None
