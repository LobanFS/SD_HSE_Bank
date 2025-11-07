from dataclasses import dataclass
from src.finance.domain.factories.entity_factory import EntityFactory
from src.finance.infrastructure.in_memory_repos.operation_repo import InMemoryOperationRepo
from src.finance.domain.enums import OperationType
from datetime import date
from typing import Optional

@dataclass
class CreateOperation:
    id: str
    type: OperationType
    bank_account_id: str
    date: date
    amount: float
    category_id: str
    description: Optional[str] = None

class CreateOperationHandler:
    def __init__(self, repo: InMemoryOperationRepo, factory: EntityFactory):
        self._repo = repo
        self._factory = factory

    def handle(self, cmd: CreateOperation) -> None:
        operation = self._factory.create_operation(id=cmd.id, type=cmd.type,
                                                 bank_account_id=cmd.bank_account_id,
                                                 date_=cmd.date, amount=cmd.amount,
                                                 category_id=cmd.category_id, description=cmd.description)
        self._repo.add(operation)
