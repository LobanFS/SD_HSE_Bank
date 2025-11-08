from src.finance.domain.factories.entity_factory import EntityFactory
from dataclasses import dataclass, replace
from src.finance.domain.entities import BankAccount
from src.finance.domain.repositories import IRepository

@dataclass(frozen=True)
class CreateAccount:
    id: str
    name: str
    balance: float = 0.0

class CreateAccountHandler:
    def __init__(self, repo: IRepository[BankAccount], factory: EntityFactory):
        self._repo = repo
        self._factory = factory

    def handle(self, cmd: CreateAccount) -> None:
        account = self._factory.create_account(cmd.id, cmd.name, cmd.balance)
        self._repo.add(account)

@dataclass(frozen=True)
class RenameAccount:
    id: str
    new_name: str

class RenameAccountHandler:
    def __init__(self, repo: IRepository[BankAccount]):
        self._repo = repo

    def handle(self, cmd: RenameAccount) -> None:
        account = self._repo.get(cmd.id)
        if account is None:
            raise ValueError(f"Account {cmd.id} not found")
        updated = replace(account, name=cmd.new_name)
        self._repo.update(updated)

@dataclass(frozen=True)
class DeleteAccount:
    id: str

class DeleteAccountHandler:
    def __init__(self, repo: IRepository[BankAccount]):
        self._repo = repo

    def handle(self, cmd: DeleteAccount) -> None:
        self._repo.remove(cmd.id)
