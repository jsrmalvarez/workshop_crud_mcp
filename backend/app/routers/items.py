from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models import models
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse, BatchResponse, ItemBatchCreate, ItemBatchDelete
import os
router = APIRouter(tags=["items"], prefix="/items")

@router.get("/environment", response_model=str, status_code=status.HTTP_200_OK)
def get_environment():
    return os.environ.get("ENVIRONMENT", "unknown")

# Batch operations first
@router.post("/batch", response_model=BatchResponse, status_code=status.HTTP_201_CREATED)
def create_items_batch(item_data: ItemBatchCreate, db: Session = Depends(get_db)):
    success_items = []
    failed_items = []
    
    for idx, item_create in enumerate(item_data.items):
        try:
            db_item = models.Item(**item_create.dict())
            db.add(db_item)
            db.flush()  # Flush to get the ID without committing
            success_items.append(db_item)
        except Exception as e:
            failed_items.append({
                "index": idx,
                "item": item_create.dict(),
                "error": str(e)
            })
            
    if success_items:  # Only commit if there are successful items
        db.commit()
        for item in success_items:
            db.refresh(item)
            
    return BatchResponse(success=success_items, failed=failed_items)

@router.delete("/batch", status_code=status.HTTP_200_OK, response_model=BatchResponse)
def delete_items_batch(delete_data: ItemBatchDelete, db: Session = Depends(get_db)):
    success_items = []
    failed_items = []
    
    for idx, item_id in enumerate(delete_data.item_ids):
        try:
            db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
            if db_item is None:
                raise HTTPException(status_code=404, detail="Item not found")
            success_items.append(db_item)
            db.delete(db_item)
        except Exception as e:
            failed_items.append({
                "index": idx,
                "item_id": item_id,
                "error": str(e)
            })
    
    if success_items:  # Only commit if there are successful deletions
        db.commit()
        
    return BatchResponse(success=success_items, failed=failed_items)

# Single item operations after
@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item_data: ItemCreate, db: Session = Depends(get_db)):
    db_item = models.Item(**item_data.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/", response_model=List[ItemResponse])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(models.Item).offset(skip).limit(limit).all()
    return items

@router.get("/{item_id}", response_model=ItemResponse)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.put("/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item_data: ItemUpdate, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    update_data = item_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(db_item)
    db.commit()
    return None