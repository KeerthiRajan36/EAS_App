from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RaiseMaintenanceSchema(BaseModel):

    asset_id: int
    issue_description: Optional[str] = None

class UpdateMaintenanceSchema(BaseModel):

    maintenance_status: Optional[str] = None

class MaintenanceResponse(BaseModel):

    id: int
    asset_id: int
    maintenance_status: str

