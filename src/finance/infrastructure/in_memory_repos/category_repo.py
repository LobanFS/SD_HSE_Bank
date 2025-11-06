from src.finance.domain.entities import Category
from src.finance.infrastructure.in_memory_repos.in_memory_generic import InMemoryGenericRepo

class InMemoryCategoryRepo(InMemoryGenericRepo[Category]):
    pass
