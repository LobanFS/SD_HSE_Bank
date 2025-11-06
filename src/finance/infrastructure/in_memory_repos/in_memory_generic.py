from typing import Dict, List, Optional, Generic, TypeVar

from src.finance.domain.entities import BankAccount, Category
from src.finance.domain.protocol_interfaces import IHasID
from src.finance.domain.repositories import IRepository

T = TypeVar("T", bound = IHasID)

class InMemoryGenericRepo(IRepository[T], Generic[T]):
    def __init__(self):
        self._repository: Dict[str, T] = {}

    def add(self, obj: T) -> None:
        self._repository[obj.id] = obj

    def get(self, id: str) -> Optional[T]:
        return self._repository.get(id)

    def list(self) -> List[T]:
        return list(self._repository.values())

    def update(self, obj: T) -> None:
        self._repository[obj.id] = obj

    def remove(self, id: str) -> None:
        self._repository.pop(id, None)
