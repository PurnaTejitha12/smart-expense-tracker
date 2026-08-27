from pydantic import BaseModel
from datetime import date


class Expense(BaseModel):
    id: int
    title: str
    amount: float
    category: str
    date: date
