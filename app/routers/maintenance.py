from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.schemas.maintenance import RaiseMaintenanceSchema, UpdateMaintenanceSchema

from app.services.maintenance_service import (
    raise_maintenance_request,
    update_maintenance,
    get_maintenance_history,
    get_all_maintenance_requests,
)

from app.utils.oauth2 import get_current_user

from app.utils.roles import RoleChecker

router = APIRouter(prefix="/maintenance", tags=["Maintenance"])

allow_admin_manager = RoleChecker(["Admin", "Manager"])


@router.post("/")
def create_maintenance_request(
    request: RaiseMaintenanceSchema,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    authorized: bool = Depends(allow_admin_manager),
):

    return raise_maintenance_request(request, current_user, db)


@router.put("/{maintenance_id}")
def update_maintenance_request(
    maintenance_id: int,
    request: UpdateMaintenanceSchema,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    authorized: bool = Depends(allow_admin_manager),
):

    return update_maintenance(maintenance_id, request, db)


@router.get("/history/{asset_id}")
def maintenance_history(
    asset_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):

    return get_maintenance_history(asset_id, db)


@router.get("/")
def list_maintenance_requests(
    db: Session = Depends(get_db), current_user=Depends(get_current_user)
):

    return get_all_maintenance_requests(db)
