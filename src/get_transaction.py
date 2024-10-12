from uuid import UUID

from transaction import Transaction
from transactions_repository import TransactionsRepository


class GetTransaction:
    def __init__(self, transactions_repository: TransactionsRepository) -> None:
        self._repository = transactions_repository

    def execute(self, transaction_id: UUID) -> Transaction:
        return self._repository.get_transaction(transaction_id)

