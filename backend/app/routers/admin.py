from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app import models, schemas, auth
from typing import Optional
import pandas as pd
import io

router = APIRouter()


async def get_admin_user(authorization: Optional[str] = None):
    """Dependency to verify admin access"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = authorization.split(" ")[1]
    email = auth.verify_token(token)
    
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # In production, check admin role from token payload
    return email


@router.post("/brands", response_model=schemas.Brand)
async def create_brand(
    brand_data: schemas.BrandCreate,
    db: Session = Depends(get_db),
    admin: str = Depends(get_admin_user)
):
    """Create a new brand"""
    # Check if brand already exists
    existing = db.query(models.Brand).filter(models.Brand.name == brand_data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Brand already exists")
    
    brand = models.Brand(**brand_data.dict())
    db.add(brand)
    db.commit()
    db.refresh(brand)
    
    return brand


@router.put("/brands/{brand_id}", response_model=schemas.Brand)
async def update_brand(
    brand_id: int,
    brand_data: schemas.BrandUpdate,
    db: Session = Depends(get_db),
    admin: str = Depends(get_admin_user)
):
    """Update brand information"""
    brand = db.query(models.Brand).filter(models.Brand.id == brand_id).first()
    
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    for key, value in brand_data.dict(exclude_unset=True).items():
        setattr(brand, key, value)
    
    db.commit()
    db.refresh(brand)
    
    return brand


@router.post("/products/upload-csv")
async def upload_product_csv(
    brand_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    admin: str = Depends(get_admin_user)
):
    """
    Upload product catalog via CSV
    Expected columns: product_id, title, description, category, subcategory, price,
                     available_sizes, fit_type, silhouette, neckline, sleeve_length,
                     length, rise, material, colors, image_url, affiliate_url
    """
    # Verify brand exists
    brand = db.query(models.Brand).filter(models.Brand.id == brand_id).first()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    # Read CSV
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
    
    # Required columns
    required_columns = ['product_id', 'title', 'category', 'price', 'image_url', 'affiliate_url']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required columns: {', '.join(missing_columns)}"
        )
    
    # Process each row
    products_created = 0
    products_updated = 0
    
    for _, row in df.iterrows():
        # Parse arrays (sizes and colors)
        available_sizes = []
        if 'available_sizes' in row and pd.notna(row['available_sizes']):
            available_sizes = [s.strip() for s in str(row['available_sizes']).split(',')]
        
        colors = []
        if 'colors' in row and pd.notna(row['colors']):
            colors = [c.strip() for c in str(row['colors']).split(',')]
        
        # Check if product exists
        existing = db.query(models.Product).filter(
            models.Product.product_id == str(row['product_id'])
        ).first()
        
        product_data = {
            'brand_id': brand_id,
            'product_id': str(row['product_id']),
            'title': str(row['title']),
            'description': str(row.get('description', '')),
            'category': str(row['category']),
            'subcategory': str(row.get('subcategory', '')) if pd.notna(row.get('subcategory')) else None,
            'price': float(row['price']),
            'sale_price': float(row['sale_price']) if 'sale_price' in row and pd.notna(row['sale_price']) else None,
            'available_sizes': available_sizes,
            'fit_type': str(row.get('fit_type', 'regular')),
            'silhouette': str(row.get('silhouette', '')),
            'neckline': str(row.get('neckline', '')) if pd.notna(row.get('neckline')) else None,
            'sleeve_length': str(row.get('sleeve_length', '')) if pd.notna(row.get('sleeve_length')) else None,
            'length': str(row.get('length', '')) if pd.notna(row.get('length')) else None,
            'rise': str(row.get('rise', '')) if pd.notna(row.get('rise')) else None,
            'material': str(row.get('material', '')) if pd.notna(row.get('material')) else None,
            'colors': colors,
            'image_url': str(row['image_url']),
            'affiliate_url': str(row['affiliate_url']),
            'in_stock': bool(row.get('in_stock', True)),
        }
        
        if existing:
            # Update
            for key, value in product_data.items():
                if key != 'product_id':  # Don't update product_id
                    setattr(existing, key, value)
            products_updated += 1
        else:
            # Create
            product = models.Product(**product_data)
            db.add(product)
            products_created += 1
    
    db.commit()
    
    return {
        "message": "Products imported successfully",
        "created": products_created,
        "updated": products_updated,
        "total": products_created + products_updated
    }


@router.post("/products", response_model=schemas.Product)
async def create_product(
    product_data: schemas.ProductCreate,
    db: Session = Depends(get_db),
    admin: str = Depends(get_admin_user)
):
    """Create a single product manually"""
    # Check if product already exists
    existing = db.query(models.Product).filter(
        models.Product.product_id == product_data.product_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Product already exists")
    
    product = models.Product(**product_data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    
    return product


@router.put("/products/{product_id}", response_model=schemas.Product)
async def update_product(
    product_id: int,
    product_data: schemas.ProductUpdate,
    db: Session = Depends(get_db),
    admin: str = Depends(get_admin_user)
):
    """Update product information"""
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for key, value in product_data.dict(exclude_unset=True).items():
        setattr(product, key, value)
    
    db.commit()
    db.refresh(product)
    
    return product


@router.delete("/products/{product_id}")
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    admin: str = Depends(get_admin_user)
):
    """Soft delete (deactivate) a product"""
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product.is_active = False
    db.commit()
    
    return {"message": "Product deactivated"}
