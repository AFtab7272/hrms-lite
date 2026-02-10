from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, unique=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True)
    department = Column(String)

    attendance = relationship("Attendance", back_populates="employee", cascade="all, delete")


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    status = Column(String)
    employee_id = Column(String, ForeignKey("employees.id"))

    employee = relationship("Employee", back_populates="attendance")