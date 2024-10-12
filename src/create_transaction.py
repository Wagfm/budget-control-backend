import os
from collections.abc import Sequence
from typing import Any

import psycopg_pool as pgp
from psycopg import Cursor

from transaction import Transaction


class DictRowFactory:
    def __init__(self, cursor: Cursor[Any]):
        self.fields = [c.name for c in cursor.description]

    def __call__(self, values: Sequence[Any]) -> dict[str, Any]:
        return dict(zip(self.fields, values))


class CreateTransaction:
    def __init__(self) -> None:
        self._row_factory = DictRowFactory
        self._pool = pgp.ConnectionPool(os.getenv("POSTGRES_URL"), min_size=3, max_size=10, open=True)

    def execute(self, data: dict) -> Transaction:
        transaction = Transaction(**data)
        query = """
            INSERT INTO public.transactions (id, amount, date, type, category, description)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING *;
        """
        parameters = [
            transaction.id, transaction.amount, transaction.date, transaction.type, transaction.category,
            transaction.description
        ]
        with self._pool.connection() as connection:
            cursor = connection.cursor(row_factory=self._row_factory)
            result = cursor.execute(query, parameters)
            created_transaction_data = result.fetchone()
        return Transaction(**created_transaction_data)
