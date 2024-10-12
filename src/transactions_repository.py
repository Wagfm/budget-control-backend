import os
from collections.abc import Sequence
from typing import Any
from uuid import UUID

import psycopg_pool as pgp
from psycopg import Cursor

from exceptions import NotFoundException
from transaction import Transaction


class DictRowFactory:
    def __init__(self, cursor: Cursor[Any]):
        self.fields = [c.name for c in cursor.description]

    def __call__(self, values: Sequence[Any]) -> dict[str, Any]:
        return dict(zip(self.fields, values))


class TransactionsRepository:
    def __init__(self) -> None:
        self._row_factory = DictRowFactory
        self._url = os.getenv("POSTGRES_URL")
        self._pool = pgp.ConnectionPool(self._url, min_size=4, max_size=100, open=True)

    def create_transaction(self, transaction: Transaction) -> Transaction:
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

    def get_transaction(self, transaction_id: UUID) -> Transaction:
        query = """
            SELECT * FROM public.transactions WHERE id = %s;
        """
        parameters = [transaction_id]
        with self._pool.connection() as connection:
            cursor = connection.cursor(row_factory=self._row_factory)
            result = cursor.execute(query, parameters)
            transaction_data = result.fetchone()
            if transaction_data is None:
                raise NotFoundException("Transaction not found")
            return Transaction(**transaction_data)
