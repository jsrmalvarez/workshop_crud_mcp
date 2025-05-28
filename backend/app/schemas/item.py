from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_active: bool = True

class ItemCreate(ItemBase):
    pass

class ItemBatchCreate(BaseModel):
    items: List[ItemCreate]

class ItemBatchDelete(BaseModel):
    item_ids: List[int]

class ItemUpdate(ItemBase):
    title: Optional[str] = None
    is_active: Optional[bool] = None

class ItemResponse(ItemBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class BatchResponse(BaseModel):
    success: List[ItemResponse]
    failed: List[dict]