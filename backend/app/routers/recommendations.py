from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app import models, schemas
from app.routers.users import get_current_user
from app.services.recommendation_engine import get_recommendation_engine

router = APIRouter()


@router.get("/", response_model=schemas.RecommendationResponse)
async def get_recommendations(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
    occasion: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    category: Optional[str] = Query(None),
    limit: int = Query(20, le=100),
    offset: int = Query(0, ge=0)
):
    """
    Get personalized product recommendations based on body type and preferences
    """
    # Create filters
    filters = schemas.RecommendationFilters(
        occasion=occasion,
        min_price=min_price,
        max_price=max_price,
        category=category
    )
    
    # Get recommendations
    engine = get_recommendation_engine(db)
    products, total_count, body_type, explanation = engine.recommend_products(
        current_user.id,
        filters=filters,
        limit=limit,
        offset=offset
    )
    
    return schemas.RecommendationResponse(
        products=products,
        total_count=total_count,
        body_type=body_type,
        explanation=explanation
    )
