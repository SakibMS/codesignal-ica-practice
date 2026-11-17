"""
Reference solution: In-Memory Database.

Design notes
- data: key -> {field: (value, expires_at)}, where expires_at is None for
  fields that never expire.
- Expired fields are purged lazily by `_record(timestamp, key)`, which every
  method uses to read a record. Empty records are removed, so "a record
  exists" always means "it has at least one live field".
- A backup stores remaining TTLs (expires_at - backup time); restore turns
  them back into absolute expiry times relative to the restore time.
"""
from typing import List, Optional


class Database:
    def __init__(self):
        self.data = {}      # key -> {field: (value, expires_at or None)}
        self.backups = []   # [(backup_time, {key: {field: (value, remaining_ttl or None)}})]

    # ---------- helpers ----------

    def _record(self, timestamp: int, key: str) -> Optional[dict]:
        """Returns the record with expired fields removed, or None if it's gone."""
        record = self.data.get(key)
        if record is None:
            return None
        for field in [f for f, (_, exp) in record.items() if exp is not None and exp <= timestamp]:
            del record[field]
        if not record:
            del self.data[key]
            return None
        return record

    # ---------- level 1 ----------

    def set(self, timestamp: int, key: str, field: str, value: str) -> None:
        self.data.setdefault(key, {})[field] = (value, None)

    def get(self, timestamp: int, key: str, field: str) -> Optional[str]:
        record = self._record(timestamp, key)
        if record is None or field not in record:
            return None
        return record[field][0]

    def delete(self, timestamp: int, key: str, field: str) -> bool:
        record = self._record(timestamp, key)
        if record is None or field not in record:
            return False
        del record[field]
        if not record:
            del self.data[key]
        return True

    def delete_record(self, timestamp: int, key: str) -> int:
        record = self._record(timestamp, key)
        if record is None:
            return 0
        del self.data[key]
        return len(record)

    # ---------- level 2 ----------

    def scan(self, timestamp: int, key: str, prefix: str) -> List[str]:
        record = self._record(timestamp, key)
        if record is None:
            return []
        return [
            f"{field}({value})"
            for field, (value, _) in sorted(record.items())
            if field.startswith(prefix)
        ]

    def find(self, timestamp: int, field: str, value: str) -> List[str]:
        keys = []
        for key in list(self.data):
            record = self._record(timestamp, key)
            if record is not None and field in record and record[field][0] == value:
                keys.append(key)
        return sorted(keys)

    # ---------- level 3 ----------

    def set_with_ttl(self, timestamp: int, key: str, field: str, value: str, ttl: int) -> None:
        self.data.setdefault(key, {})[field] = (value, timestamp + ttl)

    def get_ttl(self, timestamp: int, key: str, field: str) -> Optional[int]:
        record = self._record(timestamp, key)
        if record is None or field not in record:
            return None
        expires_at = record[field][1]
        return -1 if expires_at is None else expires_at - timestamp

    # ---------- level 4 ----------

    def backup(self, timestamp: int) -> int:
        snapshot = {}
        for key in list(self.data):
            record = self._record(timestamp, key)
            if record is not None:
                snapshot[key] = {
                    field: (value, None if exp is None else exp - timestamp)
                    for field, (value, exp) in record.items()
                }
        self.backups.append((timestamp, snapshot))
        return len(snapshot)

    def restore(self, timestamp: int, timestamp_to_restore: int) -> bool:
        chosen = None
        for backup_time, snapshot in self.backups:  # backups are in time order
            if backup_time > timestamp_to_restore:
                break
            chosen = snapshot
        if chosen is None:
            return False
        self.data = {
            key: {
                field: (value, None if remaining is None else timestamp + remaining)
                for field, (value, remaining) in record.items()
            }
            for key, record in chosen.items()
        }
        return True
