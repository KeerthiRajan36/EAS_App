from sqlalchemy import Column, Integer, ForeignKey, String, Text
from app.database import Base
from sqlalchemy.orm import relationship


class MaintenanceRequest(Base):
    __tablename__ = "maintenance_requests"

    id = Column(Integer, primary_key=True)

    asset_id = Column(Integer, ForeignKey("assets.id"))

    issue_description = Column(Text)

    maintenance_status = Column(String(50), default="Pending")

    asset = relationship("Asset")
