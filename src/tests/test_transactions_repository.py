import unittest
from uuid import uuid4

from exceptions import NotFoundException
from tests.helpers import FakeDataGenerator
from transaction import Transaction
from transactions_repository import TransactionsRepository


class TestTransactionsRepository(unittest.TestCase):
    def setUp(self) -> None:
        self._repository = TransactionsRepository()

    def tearDown(self) -> None:
        self._repository = None

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

    def test_get_transaction(self) -> None:
        transaction = Transaction(**{
            "amount": FakeDataGenerator.positive_float(),
            "date": FakeDataGenerator.date(),
            "type": "income",
            "category": FakeDataGenerator.string(5),
            "description": None
        })
        created_transaction = self._repository.create_transaction(transaction)
        self.assertIsNotNone(created_transaction)
        retrieved_transaction = self._repository.get_transaction(created_transaction.id)
        self.assertEqual(retrieved_transaction, created_transaction)
        self.assertRaises(NotFoundException, self._repository.get_transaction, uuid4())
