from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app import models, schemas
from app.routers.users import get_current_user

router = APIRouter()


@router.get("/", response_model=list[schemas.Product])
async def get_products(
    db: Session = Depends(get_db),
    category: Optional[str] = Query(None),
    brand_id: Optional[int] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    limit: int = Query(20, le=100),
    offset: int = Query(0, ge=0)
):
    """Get products with optional filtering"""
    query = db.query(models.Product).filter(models.Product.is_active == True)
    
    if category:
        query = query.filter(models.Product.category.ilike(f"%{category}%"))
    
    if brand_id:
        query = query.filter(models.Product.brand_id == brand_id)
    
    if min_price:
        query = query.filter(models.Product.price >= min_price)
    
    if max_price:
        query = query.filter(models.Product.price <= max_price)
    
    products = query.offset(offset).limit(limit).all()
    
    return products


@router.get("/{product_id}", response_model=schemas.Product)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get single product by ID"""
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return product


@router.get("/{product_id}/affiliate-link")
async def get_affiliate_link(
    product_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get affiliate link and track click
    Returns redirect URL with tracking
    """
    from fastapi.responses import RedirectResponse
    from app.config import get_settings
    
    settings = get_settings()
    
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Track click if enabled
    if settings.affiliate_click_tracking:
        click = models.AffiliateClick(
            user_id=current_user.id,
            product_id=product_id,
            ip_address="0.0.0.0",  # Get from request in production
            user_agent="unknown"  # Get from request in production
        )
        db.add(click)
        db.commit()
    
    # Return affiliate URL
    return {"affiliate_url": product.affiliate_url}
