from transaction import Transaction
from transactions_repository import TransactionsRepository


class CreateTransaction:
    def __init__(self) -> None:
        self._transactions_repository = TransactionsRepository()

    def execute(self, data: dict) -> Transaction:
        transaction = Transaction(**data)
        return self._transactions_repository.create_transaction(transaction)
