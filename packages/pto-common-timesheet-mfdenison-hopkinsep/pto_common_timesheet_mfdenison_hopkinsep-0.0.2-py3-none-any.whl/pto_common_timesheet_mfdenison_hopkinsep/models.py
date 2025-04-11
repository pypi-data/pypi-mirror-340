from typing import Optional
from sqlmodel import SQLModel, Field

class PTO(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(index=True)
    balance: int = Field(default=0)

    def __str__(self):
        return f"PTO balance for employee {self.employee_id}: {self.balance} hours"
