from src.finance.domain.factories.entity_factory import EntityFactory
from src.finance.infrastructure.in_memory_repos.category_repo import InMemoryCategoryRepo
from src.finance.domain.enums import CategoryType
from dataclasses import dataclass, replace
from src.finance.domain.entities import Category, Operation
from src.finance.domain.repositories import IRepository

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
        category = self._factory.create_category(cmd.id, cmd.type, cmd.name)
        self._repo.add(category)

@dataclass(frozen=True)
class RenameCategory:
    id: str
    new_name: str


class RenameCategoryHandler:
    def __init__(self, repo: IRepository[Category]):
        self._repo = repo

    def handle(self, cmd: RenameCategory) -> None:
        cat = self._repo.get(cmd.id)
        if cat is None:
            raise ValueError(f"Category {cmd.id} not found")
        self._repo.update(replace(cat, name=cmd.new_name))


@dataclass(frozen=True)
class DeleteCategory:
    id: str


class DeleteCategoryHandler:

    def __init__(self, cat_repo: IRepository[Category], op_repo: IRepository[Operation]):
        self._category_repo = cat_repo
        self._operation_repo = op_repo

    def handle(self, cmd: DeleteCategory) -> None:
        category = self._category_repo.get(cmd.id)
        if category is None:
            raise ValueError(f"Category {cmd.id} not found")

        #запрещаем удаление, если используется в какой-то операции
        used = any(op.category_id == cmd.id for op in self._operation_repo.list())
        if used:
            raise ValueError(f"Category {cmd.id} is used by operations and can't be deleted")

        self._category_repo.remove(cmd.id)
