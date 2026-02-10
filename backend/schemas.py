from pydantic import BaseModel, EmailStr
from datetime import date

class EmployeeCreate(BaseModel):
    employee_id: str
    full_name: str
    email: EmailStr
    department: str


class EmployeeResponse(EmployeeCreate):
    id: int

    class Config:
        orm_mode = True


class AttendanceCreate(BaseModel):
    employee_id: str
    date: date
    status: str


class AttendanceResponse(AttendanceCreate):
    id: int

    class Config:
        orm_mode = True
class AttendanceCreate(BaseModel):
    employee_id: str
    date: date
    status: str  # Present / Absent


class AttendanceResponse(AttendanceCreate):
    id: int

    class Config:
        orm_mode = True
