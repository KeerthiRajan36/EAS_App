from pydantic import BaseModel


class AssetCreate(BaseModel):
    asset_tag: str
    asset_name: str
    category: str


class AssetUpdate(BaseModel):
    asset_tag: str
    asset_name: str
    category: str
    status: str
    is_deleted: bool


class AssetResponse(BaseModel):

    id: int
    asset_tag: str
    asset_name: str
    category: str
    status: str


