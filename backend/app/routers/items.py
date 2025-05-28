from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models import models
from app.schemas import item

router = APIRouter(tags=["items"])

@router.post("/items/", response_model=item.ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item_data: item.ItemCreate, db: Session = Depends(get_db)):
    db_item = models.Item(**item_data.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.post("/items/batch", response_model=item.BatchResponse, status_code=status.HTTP_201_CREATED)
def create_items_batch(item_data: item.ItemBatchCreate, db: Session = Depends(get_db)):
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
            
    return item.BatchResponse(success=success_items, failed=failed_items)

@router.get("/items/", response_model=List[item.ItemResponse])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(models.Item).offset(skip).limit(limit).all()
    return items

@router.get("/items/{item_id}", response_model=item.ItemResponse)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.put("/items/{item_id}", response_model=item.ItemResponse)
def update_item(item_id: int, item_data: item.ItemUpdate, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    update_data = item_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(db_item)
    db.commit()
    return None

@router.delete("/items/batch", status_code=status.HTTP_200_OK, response_model=item.BatchResponse)
def delete_items_batch(delete_data: item.ItemBatchDelete, db: Session = Depends(get_db)):
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
        
    return item.BatchResponse(success=success_items, failed=failed_items)