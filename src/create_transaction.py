from transaction import Transaction
from transactions_repository import TransactionsRepository


class CreateTransaction:
    def __init__(self, transaction_repository: TransactionsRepository) -> None:
        self._transactions_repository = transaction_repository

    def execute(self, data: dict) -> Transaction:
        transaction = Transaction(**data)
        return self._transactions_repository.create_transaction(transaction)
