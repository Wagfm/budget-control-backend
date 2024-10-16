import unittest
from uuid import uuid4

from create_transaction import CreateTransaction
from exceptions import NotFoundException
from get_transaction import GetTransaction
from tests.helpers import FakeDataGenerator
from transactions_repository import TransactionsRepository


class TestGetTransactionUseCase(unittest.TestCase):
    def setUp(self) -> None:
        self._transactions_repository = TransactionsRepository()
        self._create_transaction_use_case = CreateTransaction(self._transactions_repository)
        self._get_transaction_use_case = GetTransaction(self._transactions_repository)

    def tearDown(self) -> None:
        self._transactions_repository.clear()
        self._create_transaction_use_case = None
        self._get_transaction_use_case = None

    def test_get_transaction_use_case(self) -> None:
        transaction_data = {
            "amount": FakeDataGenerator.positive_float(),
            "date": FakeDataGenerator.date(),
            "type": "income",
            "category": FakeDataGenerator.string(5),
            "description": None
        }
        created_transaction = self._create_transaction_use_case.execute(transaction_data)
        self.assertIsNotNone(created_transaction)
        self.assertRaises(NotFoundException, self._get_transaction_use_case.execute, uuid4())
        retrieved_transaction = self._get_transaction_use_case.execute(created_transaction.id)
        self.assertEqual(created_transaction, retrieved_transaction)
