from src.finance.domain.entities import BankAccount
from src.finance.infrastructure.in_memory_repos.in_memory_generic import InMemoryGenericRepo

class InMemoryAccountRepo(InMemoryGenericRepo[BankAccount]):
    pass
