from dataclasses import dataclass
from src.finance.domain.factories.entity_factory import EntityFactory
from src.finance.infrastructure.in_memory_repos.account_repo import InMemoryAccountRepo

@dataclass(frozen=True)
class CreateAccount:
    id: str
    name: str
    balance: float = 0.0

class CreateAccountHandler:
    def __init__(self, repo: InMemoryAccountRepo, factory: EntityFactory):
        self._repo = repo
        self._factory = factory

    def handle(self, cmd: CreateAccount) -> None:
        account = self._factory.create_account(cmd.id, cmd.name, cmd.balance)
        self._repo.add(account)
