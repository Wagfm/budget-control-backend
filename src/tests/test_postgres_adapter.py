import random
import unittest
import uuid

from postgres_adapter import PostgresAdapter
from tests.helpers import FakeDataGenerator
from transactions_repository import DictRowFactory


class TestPostgresAdapter(unittest.TestCase):
    def setUp(self) -> None:
        row_factory = DictRowFactory
        self._adapter = PostgresAdapter[dict](row_factory)

    def tearDown(self) -> None:
        self._adapter.clear_table("transactions")
        self._adapter = None

    def test_one(self) -> None:
        query = """
            INSERT INTO public.transactions (id, amount, date, type, category, description) 
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING *;
        """
        parameters = [
            uuid.uuid4(),
            FakeDataGenerator.positive_float(),
            FakeDataGenerator.date(),
            "expense",
            FakeDataGenerator.string(10),
            FakeDataGenerator.string(30)
        ]
        data = self._adapter.one(query, parameters)
        self.assertIsInstance(data, dict)
        self.assertAlmostEqual(parameters[1], float(data["amount"]))
        parameters.pop(1)
        data.pop("amount")
        self.assertEqual(parameters, list(data.values()))

    def test_many(self) -> None:
        batch_size = random.randint(10, 25)
        total_items = random.randint(50, 100)
        self._populate_database(total_items)
        query = """
            SELECT * FROM public.transactions;
        """
        for iteration, batch in enumerate(self._adapter.many(query, batch_size, None)):
            expected_items = min(batch_size, max(0, total_items - (iteration * batch_size)))
            self.assertEqual(expected_items, len(batch))

    def test_all(self) -> None:
        total_items = random.randint(10, 100)
        self._populate_database(total_items)
        query = """
            SELECT * FROM public.transactions;
        """
        self.assertEqual(total_items, len(self._adapter.all(query, None)))

    def _populate_database(self, k: int):
        query = """
            INSERT INTO public.transactions (id, amount, date, type, category, description) 
            VALUES (%s, %s, %s, %s, %s, %s);
        """
        parameters_arrays = []
        for i in range(k):
            parameters_arrays.append([
                uuid.uuid4(),
                FakeDataGenerator.positive_float(),
                FakeDataGenerator.date(),
                "expense",
                FakeDataGenerator.string(10),
                FakeDataGenerator.string(30)
            ])
        [self._adapter.execute(query, parameters) for parameters in parameters_arrays]
