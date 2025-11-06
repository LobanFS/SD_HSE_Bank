from dataclasses import dataclass
from src.finance.domain.factory import EntityFactory
from src.finance.infrastructure.in_memory_repos.category_repo import InMemoryCategoryRepo
from src.finance.domain.enums import CategoryType

@dataclass
class CreateCategory:
    id: str
    type: CategoryType
    name: str

class CreateCategoryHandler:
    def __init__(self, repo: InMemoryCategoryRepo, factory: EntityFactory):
        self._repo = repo
        self._factory = factory

    def handle(self, cmd: CreateCategory) -> None:
        category = self._factory.create_category(cmd.id, cmd.name, cmd.balance)
        self._repo.add(category)
