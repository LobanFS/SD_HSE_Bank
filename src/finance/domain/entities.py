from dataclasses import dataclass
from typing import Optional

@dataclass(frozen = True, slots = True)
class BankAccount:
    id: str
    name: str
    balance: float = 0.0

@dataclass(frozen = True, slots = True)
class Category:
    id: str
    #type:
    name: str

@dataclass(frozen = True, slots = True)
class Operation:
    id: str
    #type
    bank_account_id: str
    amount: float = 0.0
    description: Optional[str] = None


