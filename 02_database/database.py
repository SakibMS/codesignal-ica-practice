from typing import Optional


class Database:
    """
    In-memory database. The task is described in spec/level1.md.
    Add the methods for later levels as you unlock them.
    """

    def __init__(self):
        # TODO: set up your data structures
        pass

    def set(self, timestamp: int, key: str, field: str, value: str) -> None:
        """
        Sets `field` of record `key` to `value`, creating the record if needed.
        """
        # TODO: implement this method
        pass

    def get(self, timestamp: int, key: str, field: str) -> Optional[str]:
        """
        :return: the field's value, or None if the record or field doesn't exist.
        """
        # TODO: implement this method
        return None

    def delete(self, timestamp: int, key: str, field: str) -> bool:
        """
        Removes the field.

        :return: True if the field existed, False otherwise.
        """
        # TODO: implement this method
        return False

    def delete_record(self, timestamp: int, key: str) -> int:
        """
        Removes the whole record.

        :return: how many fields it had (0 if it doesn't exist).
        """
        # TODO: implement this method
        return 0
