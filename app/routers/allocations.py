from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.schemas.allocation import (
    AssignAssetSchema,
    ReturnAssetsSchema
)

from app.services.allocation_service import (
    assign_asset,
    return_asset,
    get_asset_history
)

from app.utils.oauth2 import (
    get_current_user
)

from app.utils.roles import (
    RoleChecker
)

router = APIRouter(
    prefix="/allocations",
    tags=["Asset Allocation"]
)

allow_admin_manager = RoleChecker([
    "Admin",
    "Manager"
])

@router.post("/assign")
def assign_asset_to_employee(
    request: AssignAssetSchema,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    authorized: bool = Depends(
        allow_admin_manager
    )
):

    return assign_asset(
        request,
        current_user,
        db
    )

@router.post("/return")
def return_assigned_asset(
    request: ReturnAssetsSchema,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    authorized: bool = Depends(
        allow_admin_manager
    )
):

    return return_asset(
        request,
        db
    )

@router.get("/history/{asset_id}")
def view_asset_history(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return get_asset_history(
        asset_id,
        db
    )