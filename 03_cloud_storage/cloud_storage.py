from typing import Optional


class CloudStorage:
    """
    Cloud file storage. The task is described in spec/level1.md.
    Add the methods for later levels as you unlock them.
    """

    def __init__(self):
        # TODO: set up your data structures
        pass

    def add_file(self, timestamp: int, name: str, size: int) -> bool:
        """
        Adds a new file.

        :return: True if added, False if a file with that name already exists.
        """
        # TODO: implement this method
        return False

    def get_file_size(self, timestamp: int, name: str) -> Optional[int]:
        """
        :return: the file's size, or None if it doesn't exist.
        """
        # TODO: implement this method
        return None

    def delete_file(self, timestamp: int, name: str) -> Optional[int]:
        """
        Deletes the file.

        :return: the deleted file's size, or None if it doesn't exist.
        """
        # TODO: implement this method
        return None

    def copy_file(self, timestamp: int, source: str, dest: str) -> bool:
        """
        Creates `dest` as a copy of `source`.

        :return: True on success, False if `source` doesn't exist
                 or `dest` already exists.
        """
        # TODO: implement this method
        return False
