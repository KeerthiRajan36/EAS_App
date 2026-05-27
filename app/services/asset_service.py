from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.asset import Asset
from app.schemas.asset import AssetCreate

VALID_STATUS = ["Available", "Assigned", "Maintenance", "Retired"]


def create_asset(request:AssetCreate, db: Session):
    existing_assest = (
        db.query(Asset).filter(request.asset_tag == request.asset_tag).first()
    )

    if existing_assest:
        raise HTTPException(status_code=400, detail="Asset tag already exists")

    asset = Asset(
        asset_tag=request.asset_tag,
        assest_name=request.asset_name,
        category=request.category,
    )

    db.add(asset)
    db.commit()
    db.refresh(asset)

    return asset


def update_asset(asset_id, request, db: Session):

    asset = (
        db.query(Asset).filter(Asset.id == asset_id, Asset.is_deleted == False).first()
    )

    if not asset:

        raise HTTPException(status_code=404, detail="Asset not found")

    update_data = request.dict(exclude_unset=True)

    if "status" in update_data:

        if update_data["status"] not in VALID_STATUS:

            raise HTTPException(status_code=400, detail="Invalid status")

    for key, value in update_data.items():

        setattr(asset, key, value)

    db.commit()

    db.refresh(asset)

    return asset


def soft_delete_asset(asset_id, db: Session):

    asset = (
        db.query(Asset).filter(Asset.id == asset_id, Asset.is_deleted == False).first()
    )

    if not asset:

        raise HTTPException(status_code=404, detail="Asset not found")

    asset.is_deleted = True

    db.commit()

    return {"message": "Asset deleted successfully"}


def get_all_assets(db: Session):

    return db.query(Asset).filter(Asset.is_deleted == False).all()


def get_asset_by_id(asset_id, db: Session):

    asset = (
        db.query(Asset).filter(Asset.id == asset_id, Asset.is_deleted == False).first()
    )

    if not asset:

        raise HTTPException(status_code=404, detail="Asset not found")

    return asset
