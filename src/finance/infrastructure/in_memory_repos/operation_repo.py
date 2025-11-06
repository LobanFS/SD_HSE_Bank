from src.finance.domain.entities import Operation
from src.finance.infrastructure.in_memory_repos.in_memory_generic import InMemoryGenericRepo

class InMemoryOperationRepo(InMemoryGenericRepo[Operation]):
    pass
