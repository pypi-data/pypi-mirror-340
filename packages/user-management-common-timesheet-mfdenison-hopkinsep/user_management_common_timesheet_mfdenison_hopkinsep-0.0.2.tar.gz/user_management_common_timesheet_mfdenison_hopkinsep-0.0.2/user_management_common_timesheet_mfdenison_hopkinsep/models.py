from typing import Optional, List
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, String

# Define an Enum for role choices.
class RoleEnum(str, Enum):
    Employee = "Employee"
    Manager = "Manager"
    HR = "HR"

class Employee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # New fields for authentication:
    username: str = Field(
        sa_column=Column(String(100), unique=True, index=True),
        description="Unique username for logging in"
    )
    hashed_password: str = Field(
        sa_column=Column(String(200)),
        description="Hashed password for authentication"
    )

    # Other fields:
    name: str = Field(sa_column=Column(String(100)))
    role: RoleEnum = Field(sa_column=Column(String(50)))
    department: str = Field(sa_column=Column(String(100)))

    # Self-reference: manager_id is a foreign key to Employee.id (can be null)
    manager_id: Optional[int] = Field(default=None, foreign_key="employee.id", nullable=True)

    # Relationship to self: an Employee may have a manager.
    manager: Optional["Employee"] = Relationship(
        back_populates="subordinates",
        sa_relationship_kwargs={"remote_side": "Employee.id"}
    )
    # Relationship to self: a manager may have many subordinates.
    subordinates: List["Employee"] = Relationship(back_populates="manager")

    def __str__(self) -> str:
        return self.name
