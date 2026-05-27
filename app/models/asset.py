from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    asset_tag = Column(String(100), unique=True)
    asset_name = Column(String(255))
    category = Column(String(100))
    status = Column(String(50), default="Available")
    is_deleted = Column(Boolean, default=False)
