import datetime as dt
import unittest

from tests.helpers import FakeDataGenerator
from transaction import Transaction


class TestTransaction(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_valid_transaction(self) -> None:
        transaction_data_1 = {
            "amount": FakeDataGenerator.float(),
            "date": FakeDataGenerator.date(),
            "type": "income",
            "category": FakeDataGenerator.string(5),
            "description": None
        }
        transaction_data_2 = {
            "amount": FakeDataGenerator.float(),
            "date": FakeDataGenerator.date(),
            "type": "expense",
            "category": FakeDataGenerator.string(5),
            "description": None
        }
        transaction_data_3 = {
            "amount": FakeDataGenerator.float(),
            "date": FakeDataGenerator.date(),
            "type": "income",
            "category": FakeDataGenerator.string(5),
            "description": FakeDataGenerator.string(100)
        }
        self._validate_transaction(transaction_data_1)
        self._validate_transaction(transaction_data_2)
        self._validate_transaction(transaction_data_3)

    def _validate_transaction(self, transaction_data: dict) -> None:
        transaction = Transaction(**transaction_data)
        self.assertEqual(transaction.model_dump(exclude={"id"}), transaction_data)
        self.assertIsInstance(transaction.amount, float)
        self.assertIsInstance(transaction.date, dt.date)
        self.assertIsInstance(transaction.type, str)
        self.assertIsInstance(transaction.category, str)
