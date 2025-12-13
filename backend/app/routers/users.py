from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app import models, schemas, auth

router = APIRouter()


async def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> models.User:
    """Dependency to get current authenticated user"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    token = authorization.split(" ")[1]
    email = auth.verify_token(token)
    
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    user = db.query(models.User).filter(models.User.email == email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@router.get("/me", response_model=schemas.User)
async def get_current_user_info(
    current_user: models.User = Depends(get_current_user)
):
    """Get current user info"""
    return current_user


@router.post("/me/profile", response_model=schemas.UserProfile)
async def create_or_update_profile(
    profile_data: schemas.UserProfileCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create or update user profile and preferences"""
    # Check if profile exists
    profile = db.query(models.UserProfile).filter(
        models.UserProfile.user_id == current_user.id
    ).first()
    
    if profile:
        # Update existing profile
        for key, value in profile_data.dict(exclude_unset=True).items():
            setattr(profile, key, value)
    else:
        # Create new profile
        profile = models.UserProfile(
            user_id=current_user.id,
            **profile_data.dict()
        )
        db.add(profile)
    
    db.commit()
    db.refresh(profile)
    
    return profile


@router.get("/me/profile", response_model=schemas.UserProfile)
async def get_profile(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user profile"""
    profile = db.query(models.UserProfile).filter(
        models.UserProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    return profile


@router.delete("/me")
async def delete_account(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete user account and all associated data (GDPR compliance)"""
    from app.services.storage import get_storage_service
    
    # Delete photos from storage
    storage = get_storage_service()
    storage.delete_user_photos(current_user.id)
    
    # Delete from database (cascade will handle related records)
    db.delete(current_user)
    db.commit()
    
    return {"message": "Account deleted successfully"}


@router.get("/me/favorites", response_model=list[schemas.Product])
async def get_favorites(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's favorite products"""
    favorites = db.query(models.Favorite).filter(
        models.Favorite.user_id == current_user.id
    ).all()
    
    product_ids = [fav.product_id for fav in favorites]
    products = db.query(models.Product).filter(
        models.Product.id.in_(product_ids)
    ).all()
    
    return products


@router.post("/me/favorites/{product_id}")
async def add_favorite(
    product_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add product to favorites"""
    # Check if already favorited
    existing = db.query(models.Favorite).filter(
        models.Favorite.user_id == current_user.id,
        models.Favorite.product_id == product_id
    ).first()
    
    if existing:
        return {"message": "Already in favorites"}
    
    favorite = models.Favorite(
        user_id=current_user.id,
        product_id=product_id
    )
    db.add(favorite)
    db.commit()
    
    return {"message": "Added to favorites"}


@router.delete("/me/favorites/{product_id}")
async def remove_favorite(
    product_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove product from favorites"""
    favorite = db.query(models.Favorite).filter(
        models.Favorite.user_id == current_user.id,
        models.Favorite.product_id == product_id
    ).first()
    
    if not favorite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Favorite not found"
        )
    
    db.delete(favorite)
    db.commit()
    
    return {"message": "Removed from favorites"}


@router.get("/me/lookbooks", response_model=list[schemas.Lookbook])
async def get_lookbooks(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's lookbooks"""
    lookbooks = db.query(models.Lookbook).filter(
        models.Lookbook.user_id == current_user.id
    ).all()
    
    return lookbooks


@router.post("/me/lookbooks", response_model=schemas.Lookbook)
async def create_lookbook(
    lookbook_data: schemas.LookbookCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new lookbook"""
    lookbook = models.Lookbook(
        user_id=current_user.id,
        **lookbook_data.dict()
    )
    
    db.add(lookbook)
    db.commit()
    db.refresh(lookbook)
    
    return lookbook
