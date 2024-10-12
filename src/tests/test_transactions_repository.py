import unittest

from tests.helpers import FakeDataGenerator
from transaction import Transaction
from transactions_repository import TransactionsRepository


class TestTransactionsRepository(unittest.TestCase):
    def setUp(self) -> None:
        self._repository = TransactionsRepository()

    def tearDown(self) -> None:
        pass

    def test_create_transaction(self) -> None:
        transaction = Transaction(**{
            "amount": FakeDataGenerator.positive_float(),
            "date": FakeDataGenerator.date(),
            "type": "income",
            "category": FakeDataGenerator.string(5),
            "description": None
        })
        created_transaction = self._repository.create_transaction(transaction)
        self.assertEqual(created_transaction.model_dump(exclude={"amount"}), transaction.model_dump(exclude={"amount"}))
        self.assertAlmostEqual(created_transaction.amount, transaction.amount)
