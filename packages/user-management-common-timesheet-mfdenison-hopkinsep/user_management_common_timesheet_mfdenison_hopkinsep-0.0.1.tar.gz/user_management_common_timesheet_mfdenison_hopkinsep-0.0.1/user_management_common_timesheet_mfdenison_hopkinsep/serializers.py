from typing import Optional, List
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, String

class RoleEnum(str, Enum):
    Employee = "Employee"
    Manager = "Manager"
    HR = "HR"

class Employee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", unique=True)
    name: str = Field(sa_column=Column(String(100)))
    role: RoleEnum = Field(sa_column=Column(String(50)))
    department: str = Field(sa_column=Column(String(100)))
    manager_id: Optional[int] = Field(default=None, foreign_key="employee.id", nullable=True)
    manager: Optional["Employee"] = Relationship(
        back_populates="subordinates",
        sa_relationship_kwargs={"remote_side": "Employee.id"}
    )
    subordinates: List["Employee"] = Relationship(back_populates="manager")

    def __str__(self) -> str:
        return self.name
