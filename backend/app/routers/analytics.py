from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.database import get_db
from app import models, schemas
from app.routers.admin import get_admin_user
from datetime import datetime, timedelta

router = APIRouter()


@router.get("/overview", response_model=schemas.AnalyticsOverview)
async def get_analytics_overview(
    db: Session = Depends(get_db),
    admin: str = Depends(get_admin_user)
):
    """Get analytics overview for admin dashboard"""
    
    # Total clicks
    total_clicks = db.query(func.count(models.AffiliateClick.id)).scalar()
    
    # Total conversions
    total_conversions = db.query(func.count(models.AffiliateClick.id)).filter(
        models.AffiliateClick.converted == True
    ).scalar()
    
    # Conversion rate
    conversion_rate = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
    
    # Total commission earned
    total_commission = db.query(func.sum(models.AffiliateClick.commission_earned)).filter(
        models.AffiliateClick.converted == True
    ).scalar() or 0
    
    # Top products by clicks
    top_products_query = (
        db.query(
            models.Product.id,
            models.Product.title,
            func.count(models.AffiliateClick.id).label('clicks')
        )
        .join(models.AffiliateClick)
        .group_by(models.Product.id, models.Product.title)
        .order_by(desc('clicks'))
        .limit(10)
        .all()
    )
    
    top_products = [
        {"product_id": p.id, "title": p.title, "clicks": p.clicks}
        for p in top_products_query
    ]
    
    # Top categories by clicks
    top_categories_query = (
        db.query(
            models.Product.category,
            func.count(models.AffiliateClick.id).label('clicks')
        )
        .join(models.AffiliateClick)
        .group_by(models.Product.category)
        .order_by(desc('clicks'))
        .limit(10)
        .all()
    )
    
    top_categories = [
        {"category": c.category, "clicks": c.clicks}
        for c in top_categories_query
    ]
    
    return schemas.AnalyticsOverview(
        total_clicks=total_clicks,
        total_conversions=total_conversions,
        conversion_rate=round(conversion_rate, 2),
        total_commission_earned=float(total_commission),
        top_products=top_products,
        top_categories=top_categories
    )


@router.get("/clicks")
async def get_recent_clicks(
    db: Session = Depends(get_db),
    admin: str = Depends(get_admin_user),
    limit: int = 50
):
    """Get recent affiliate clicks"""
    clicks = (
        db.query(models.AffiliateClick)
        .order_by(models.AffiliateClick.clicked_at.desc())
        .limit(limit)
        .all()
    )
    
    return clicks
