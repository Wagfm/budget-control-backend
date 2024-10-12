import unittest

from create_transaction import CreateTransaction
from tests.helpers import FakeDataGenerator
from transactions_repository import TransactionsRepository


class TestCreateTransactionUseCase(unittest.TestCase):
    def setUp(self) -> None:
        transactions_repository = TransactionsRepository()
        self._create_transaction_use_case = CreateTransaction(transactions_repository)

    def tearDown(self) -> None:
        self._create_transaction_use_case = None

    def test_create_valid_transaction(self) -> None:
        transaction_data = {
            "amount": FakeDataGenerator.positive_float(),
            "date": FakeDataGenerator.date(),
            "type": "income",
            "category": FakeDataGenerator.string(5),
            "description": None
        }
        created_transaction = self._create_transaction_use_case.execute(transaction_data)
        data_to_compare = transaction_data.copy()
        amount = data_to_compare.pop("amount")
        self.assertEqual(created_transaction.model_dump(exclude={"amount", "id"}), data_to_compare)
        self.assertAlmostEqual(created_transaction.amount, amount)
