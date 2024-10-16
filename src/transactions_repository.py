import os
from uuid import UUID

import psycopg_pool as pgp

from exceptions import NotFoundException
from postgres_dict_row_factory import DictRowFactory
from transaction import Transaction


class TransactionsRepository:
    def __init__(self) -> None:
        self._row_factory = DictRowFactory
        self._url = os.getenv("POSTGRES_URL")
        self._pool = pgp.ConnectionPool(self._url, min_size=4, max_size=100, open=True)
        self._create_table()

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
            with connection.cursor(row_factory=self._row_factory) as cursor:
                cursor.execute(query, parameters)
                created_transaction_data = cursor.fetchone()
                return Transaction(**created_transaction_data)

    def get_transaction(self, transaction_id: UUID) -> Transaction:
        query = """
            SELECT * FROM public.transactions WHERE id = %s;
        """
        parameters = [transaction_id]
        with self._pool.connection() as connection:
            with connection.cursor(row_factory=self._row_factory) as cursor:
                cursor.execute(query, parameters)
                transaction_data = cursor.fetchone()
                if transaction_data is None:
                    raise NotFoundException("Transaction not found")
                return Transaction(**transaction_data)

    def clear(self) -> None:
        query = """
            DELETE FROM public.transactions;
        """
        with self._pool.connection() as connection:
            with connection.cursor(row_factory=self._row_factory) as cursor:
                cursor.execute(query)

    def _create_table(self) -> None:
        query = """
            CREATE TABLE IF NOT EXISTS public.transactions (
                id UUID PRIMARY KEY,
                amount NUMERIC NOT NULL,
                date DATE NOT NULL,
                type VARCHAR(15) NOT NULL,
                category VARCHAR(25) NOT NULL,
                description VARCHAR(100)
            );
        """
        with self._pool.connection() as connection:
            with connection.cursor(row_factory=self._row_factory) as cursor:
                cursor.execute(query)
