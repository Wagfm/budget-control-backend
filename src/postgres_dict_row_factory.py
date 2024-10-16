from collections.abc import Sequence
from typing import Any

from psycopg import Cursor


class DictRowFactory:
    def __init__(self, cursor: Cursor[Any]):
        self.fields = [c.name for c in cursor.description] if cursor.description is not None else []

    def __call__(self, values: Sequence[Any]) -> dict[str, Any]:
        return dict(zip(self.fields, values))
