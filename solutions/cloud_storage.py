"""
Reference solution: Cloud Storage.

Design notes
- files: name -> {"owner": user_id, "versions": [size, ...]}. The current size
  is versions[-1] and the version number is len(versions). Storing the
  history from the start makes level 4 cheap.
- users: user_id -> {"capacity", "used"}. "used" is kept up to date on every
  add / delete / copy / update, so capacity checks are O(1).
- The built-in "admin" owns files from add_file and has no limit.
"""
from typing import List, Optional

ADMIN = "admin"


class CloudStorage:
    def __init__(self):
        self.files = {}  # name -> {"owner": str, "versions": [size, ...]}
        self.users = {}  # user_id -> {"capacity": int, "used": int}

    # ---------- helpers ----------

    def _fits(self, owner: str, extra: int) -> bool:
        if owner == ADMIN:
            return True
        user = self.users[owner]
        return user["used"] + extra <= user["capacity"]

    def _change_usage(self, owner: str, delta: int) -> None:
        if owner != ADMIN:
            self.users[owner]["used"] += delta

    def _create(self, owner: str, name: str, size: int) -> None:
        self.files[name] = {"owner": owner, "versions": [size]}
        self._change_usage(owner, size)

    # ---------- level 1 ----------

    def add_file(self, timestamp: int, name: str, size: int) -> bool:
        if name in self.files:
            return False
        self._create(ADMIN, name, size)
        return True

    def get_file_size(self, timestamp: int, name: str) -> Optional[int]:
        file = self.files.get(name)
        return None if file is None else file["versions"][-1]

    def delete_file(self, timestamp: int, name: str) -> Optional[int]:
        file = self.files.pop(name, None)
        if file is None:
            return None
        size = file["versions"][-1]
        self._change_usage(file["owner"], -size)
        return size

    def copy_file(self, timestamp: int, source: str, dest: str) -> bool:
        file = self.files.get(source)
        if file is None or dest in self.files:
            return False
        size = file["versions"][-1]
        if not self._fits(file["owner"], size):
            return False
        self._create(file["owner"], dest, size)
        return True

    # ---------- level 2 ----------

    def find_files(self, timestamp: int, prefix: str, suffix: str) -> List[str]:
        matches = sorted(
            (-file["versions"][-1], name)
            for name, file in self.files.items()
            if name.startswith(prefix) and name.endswith(suffix)
        )
        return [f"{name}({-neg_size})" for neg_size, name in matches[:10]]

    def total_size(self, timestamp: int, prefix: str) -> int:
        return sum(
            file["versions"][-1] for name, file in self.files.items() if name.startswith(prefix)
        )

    # ---------- level 3 ----------

    def add_user(self, timestamp: int, user_id: str, capacity: int) -> bool:
        if user_id in self.users:
            return False
        self.users[user_id] = {"capacity": capacity, "used": 0}
        return True

    def add_file_by(self, timestamp: int, user_id: str, name: str, size: int) -> Optional[int]:
        user = self.users.get(user_id)
        if user is None or name in self.files or not self._fits(user_id, size):
            return None
        self._create(user_id, name, size)
        return user["capacity"] - user["used"]

    def update_capacity(self, timestamp: int, user_id: str, capacity: int) -> Optional[int]:
        user = self.users.get(user_id)
        if user is None:
            return None
        user["capacity"] = capacity
        owned = sorted(
            (-file["versions"][-1], name)
            for name, file in self.files.items()
            if file["owner"] == user_id
        )
        removed = 0
        for _, name in owned:
            if user["used"] <= capacity:
                break
            self.delete_file(timestamp, name)
            removed += 1
        return removed

    # ---------- level 4 ----------

    def update_file(self, timestamp: int, name: str, size: int) -> Optional[int]:
        file = self.files.get(name)
        if file is None:
            return None
        delta = size - file["versions"][-1]
        if not self._fits(file["owner"], delta):
            return None
        file["versions"].append(size)
        self._change_usage(file["owner"], delta)
        return len(file["versions"])

    def get_version(self, timestamp: int, name: str) -> Optional[int]:
        file = self.files.get(name)
        return None if file is None else len(file["versions"])

    def restore_version(self, timestamp: int, name: str, version: int) -> Optional[int]:
        file = self.files.get(name)
        if file is None or not 1 <= version <= len(file["versions"]):
            return None
        return self.update_file(timestamp, name, file["versions"][version - 1])
