import dataclasses
from dataclasses import dataclass
from datetime import datetime


@dataclasses.dataclass
class Currency:
    name: str
    code: str


@dataclasses.dataclass
class OperationAmount:
    amount: float
    currency: Currency


@dataclasses.dataclass
class Operation:
    id: int
    state: str
    date: datetime
    operation_amount: OperationAmount
    description: str
    cart_from: str | None
    cart_to: str | None
