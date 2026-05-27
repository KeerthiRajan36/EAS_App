from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.schemas.asset import AssetCreate, AssetUpdate

from app.services.asset_service import (
    create_asset,
    update_asset,
    soft_delete_asset,
    get_all_assets,
    get_asset_by_id,
)

from app.utils.oauth2 import get_current_user

from app.utils.roles import RoleChecker

router = APIRouter(prefix="/assets", tags=["Assets"])

allow_admin_manager = RoleChecker(["Admin", "Manager"])


@router.post("/create")
def add_asset(
    request: AssetCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    authorized: bool = Depends(allow_admin_manager),
):

    print(request)
    return create_asset(request, db)


@router.put("/{asset_id}")
def edit_asset(
    asset_id: int,
    request: AssetUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    authorized: bool = Depends(allow_admin_manager),
):

    return update_asset(asset_id, request, db)


@router.delete("/{asset_id}")
def delete_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    authorized: bool = Depends(allow_admin_manager),
):

    return soft_delete_asset(asset_id, db)


@router.get("/")
def list_assets(db: Session = Depends(get_db), user=Depends(get_current_user)):

    return get_all_assets(db)


@router.get("/{asset_id}")
def get_asset(
    asset_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):

    return get_asset_by_id(asset_id, db)
