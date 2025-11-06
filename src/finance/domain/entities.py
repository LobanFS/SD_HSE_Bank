from dataclasses import dataclass
from typing import Optional
from datetime import date
from src.finance.domain.enums import CategoryType, OperationType

@dataclass(frozen = True, slots = True)
class BankAccount:
    id: str
    name: str
    balance: float = 0.0

@dataclass(frozen = True, slots = True)
class Category:
    id: str
    type: CategoryType
    name: str

@dataclass(frozen = True, slots = True)
class Operation:
    id: str
    type: OperationType
    bank_account_id: str
    date: date
    amount: float
    category_id : str
    description: Optional[str] = None




