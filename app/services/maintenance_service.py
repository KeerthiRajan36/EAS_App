from datetime import datetime

from fastapi import HTTPException

from sqlalchemy.sql import func

from app.models.asset import Asset
from app.models.maintenance import MaintenanceRequest

VALID_STATUS = ["Pending", "In Progress", "Completed", "Rejected"]


def raise_maintenance_request(request, current_user, db):

    asset = (
        db.query(Asset)
        .filter(Asset.id == request.asset_id, Asset.is_deleted == False)
        .first()
    )

    if not asset:

        raise HTTPException(status_code=404, detail="Asset not found")

    maintenance = MaintenanceRequest(
        asset_id=request.asset_id,
        issue_description=request.issue_description,
    )

    asset.status = "Maintenance"

    db.add(maintenance)

    db.commit()

    db.refresh(maintenance)

    return maintenance


def update_maintenance(maintenance_id, request, db):

    maintenance = (
        db.query(MaintenanceRequest)
        .filter(MaintenanceRequest.id == maintenance_id)
        .first()
    )

    if not maintenance:

        raise HTTPException(status_code=404, detail="Maintenance request not found")

    update_data = request.dict(exclude_unset=True)

    if "maintenance_status" in update_data:

        if update_data["maintenance_status"] not in VALID_STATUS:

            raise HTTPException(status_code=400, detail="Invalid maintenance status")

    for key, value in update_data.items():

        setattr(maintenance, key, value)

    asset = db.query(Asset).filter(Asset.id == maintenance.asset_id).first()

    if maintenance.maintenance_status == "Completed":

        maintenance.completed_at = datetime.utcnow()

        asset.status = "Available"

    db.commit()

    db.refresh(maintenance)

    return maintenance


def get_maintenance_history(asset_id, db):

    asset = db.query(Asset).filter(Asset.id == asset_id).first()

    if not asset:

        raise HTTPException(status_code=404, detail="Asset not found")

    history = (
        db.query(MaintenanceRequest)
        .filter(MaintenanceRequest.asset_id == asset_id)
        .all()
    )

    return history


def get_all_maintenance_requests(db):

    return db.query(MaintenanceRequest).all()
