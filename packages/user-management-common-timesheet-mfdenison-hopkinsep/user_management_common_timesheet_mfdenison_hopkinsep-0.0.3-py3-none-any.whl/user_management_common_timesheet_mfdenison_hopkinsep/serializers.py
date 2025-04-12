from typing import Optional
from pydantic import BaseModel
from .models import RoleEnum

class EmployeeSerializer(BaseModel):
    id: Optional[int]
    username: str
    name: str
    role: RoleEnum
    department: str
    manager_id: Optional[int] = None

    class Config:
        orm_mode = True
