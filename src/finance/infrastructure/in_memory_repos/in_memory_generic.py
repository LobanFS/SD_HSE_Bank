from typing import Dict, List, Optional, Generic, TypeVar
from src.finance.domain.protocol_interfaces import IHasID
from src.finance.domain.repositories import IRepository
from src.finance.domain.errors import AlreadyExistsError, NotFoundError

T = TypeVar("T", bound = IHasID)

class InMemoryGenericRepo(IRepository[T], Generic[T]):
    def __init__(self):
        self._repository: Dict[str, T] = {}

    def add(self, obj: T) -> None:
        if obj.id in self._repository:
            raise AlreadyExistsError(f"Object with id={obj.id} already exists")
        self._repository[obj.id] = obj

    def get(self, id: str) -> Optional[T]:
        return self._repository.get(id)

    def list(self) -> List[T]:
        return list(self._repository.values())

    def update(self, obj: T) -> None:
        if obj.id not in self._repository:
            raise NotFoundError(f"Object with id={obj.id} not found")
        self._repository[obj.id] = obj

    def remove(self, id: str) -> None:
        if id not in self._repository:
            raise NotFoundError(f"Object with id={id} not found")
        del self._repository[id]

    def safe_add(self, obj) -> bool:
        try:
            self.add(obj)
            return True
        except AlreadyExistsError:
            return False
