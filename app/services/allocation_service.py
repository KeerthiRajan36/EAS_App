from fastapi import HTTPException
from sqlalchemy.sql import func
from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.models.employee import Employee
from app.models.allocation import AssetAllocation

VALID_ASSET_STATUS = ["Available", "Assigned", "Maintenance", "Retired"]


def assign_asset(request, current_user, db: Session):
    asset = (
        db.query(Asset)
        .filter(Asset.id == request.id, Asset.is_deleted == False)
        .first()
    )

    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    employee = db.query(Employee).filter(Employee.id == request.employee_id).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not Found")

    existing_allocation = (
        db.query(AssetAllocation)
        .filter(
            AssetAllocation.asset_id == request.asset_id,
            AssetAllocation.returned_date == None,
        )
        .first()
    )
    if existing_allocation:

        raise HTTPException(status_code=400, detail="Asset already assigned")

    if asset.status != "Available":

        raise HTTPException(status_code=400, detail="Asset is not available")
    allocation = AssetAllocation(
        asset_id=request.asset_id,
        employee_id=request.employee_id,
        assigned_by=current_user.id,
    )

    asset.status = "Assigned"

    db.add(allocation)

    db.commit()

    db.refresh(allocation)

    return allocation


def return_asset(request, db):

    allocation = (
        db.query(AssetAllocation)
        .filter(
            AssetAllocation.id == request.allocation_id,
            AssetAllocation.returned_date == None,
        )
        .first()
    )

    if not allocation:

        raise HTTPException(status_code=404, detail="Active allocation not found")

    asset = db.query(Asset).filter(Asset.id == allocation.asset_id).first()

    allocation.returned_date = func.now()

    allocation.allocation_status = "Returned"

    asset.status = "Available"

    db.commit()

    return {"message": "Asset returned successfully"}


def get_asset_history(asset_id, db):

    asset = db.query(Asset).filter(Asset.id == asset_id).first()

    if not asset:

        raise HTTPException(status_code=404, detail="Asset not found")

    history = (
        db.query(AssetAllocation).filter(AssetAllocation.asset_id == asset_id).all()
    )

    return history
