import os
from collections.abc import Generator
from typing import Any, Optional

from psycopg.rows import RowFactory
from psycopg_pool import ConnectionPool


class PostgresAdapter[T]:
    def __init__(self, row_factory: RowFactory) -> None:
        self._row_factory = row_factory
        self._url = os.getenv("POSTGRES_URL")
        self._pool = ConnectionPool(self._url, min_size=4, max_size=100, open=True)

    def execute(self, query: str, parameters: Optional[list[Any]] = None) -> None:
        with self._pool.connection() as connection:
            with connection.cursor(row_factory=self._row_factory) as cursor:
                cursor.execute(query, parameters)

    def one(self, query: str, parameters: Optional[list[Any]] = None) -> T:
        with self._pool.connection() as connection:
            with connection.cursor(row_factory=self._row_factory) as cursor:
                cursor.execute(query, parameters)
                return cursor.fetchone()

    def many(self, query: str, n: int, parameters: Optional[list[Any]] = None) -> Generator[list[T]]:
        with self._pool.connection() as connection:
            with connection.cursor(row_factory=self._row_factory) as cursor:
                cursor.execute(query, parameters)
                while True:
                    rows = cursor.fetchmany(n)
                    if not rows:
                        break
                    yield rows

    def all(self, query: str, parameters: Optional[list[Any]] = None) -> list[T]:
        with self._pool.connection() as connection:
            with connection.cursor(row_factory=self._row_factory) as cursor:
                cursor.execute(query, parameters)
                return cursor.fetchall()

    def clear_table(self, table_name: str) -> None:
        query = f"""
            DELETE FROM public.{table_name};
        """
        self.execute(query)
