from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.orm import relationship


class AssetAllocation(Base):
    __tablename__ = "asset_allocations"

    id = Column(Integer, primary_key=True)

    asset_id = Column(Integer, ForeignKey("assets.id"))
    employee_id = Column(Integer, ForeignKey("employees.id"))

    assigned_date = Column(DateTime, default=func.now())
    returned_date = Column(DateTime, nullable=True)
    asset = relationship("Asset")
    employee = relationship("Employee")
