from sqlalchemy import Column, Integer, String
from app.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    employee_code = Column(String(100), unique=True)
    full_name = Column(String(255))
    departname = Column(String(100))
    email = Column(String(255))
