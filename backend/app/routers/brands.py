from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter()


@router.get("/", response_model=list[schemas.Brand])
async def get_brands(
    db: Session = Depends(get_db),
    active_only: bool = True
):
    """Get all brands"""
    query = db.query(models.Brand)
    
    if active_only:
        query = query.filter(models.Brand.is_active == True)
    
    brands = query.all()
    
    return brands


@router.get("/{brand_id}", response_model=schemas.Brand)
async def get_brand(brand_id: int, db: Session = Depends(get_db)):
    """Get single brand by ID"""
    brand = db.query(models.Brand).filter(models.Brand.id == brand_id).first()
    
    if not brand:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Brand not found")
    
    return brand
