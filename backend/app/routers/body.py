from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.routers.users import get_current_user
from app.services.body_analyzer import get_body_analyzer
from app.services.storage import get_storage_service
import os
import tempfile

router = APIRouter()


@router.post("/analyze", response_model=schemas.BodyAnalysisResult)
async def analyze_body(
    front_photo: UploadFile = File(...),
    side_photo: UploadFile = File(None),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Analyze body from photos and return body type with recommendations
    Photos are deleted after processing unless user opted in to storage
    """
    analyzer = get_body_analyzer()
    storage = get_storage_service()
    
    # Get user profile to check storage preference
    profile = db.query(models.UserProfile).filter(
        models.UserProfile.user_id == current_user.id
    ).first()
    
    store_photos = profile.store_photos if profile else False
    
    # Save photos temporarily
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save front photo
        front_path = os.path.join(temp_dir, "front.jpg")
        with open(front_path, "wb") as f:
            f.write(await front_photo.read())
        
        # Save side photo if provided
        side_path = None
        if side_photo:
            side_path = os.path.join(temp_dir, "side.jpg")
            with open(side_path, "wb") as f:
                f.write(await side_photo.read())
        
        try:
            # Analyze body
            result = analyzer.analyze_body(front_path, side_path)
            
            # Save to database
            photo_front_url = None
            photo_side_url = None
            
            if store_photos:
                # Upload to storage
                with open(front_path, "rb") as f:
                    photo_front_url = storage.upload_photo(
                        current_user.id,
                        f.read(),
                        "front",
                        store_permanently=True
                    )
                
                if side_path:
                    with open(side_path, "rb") as f:
                        photo_side_url = storage.upload_photo(
                            current_user.id,
                            f.read(),
                            "side",
                            store_permanently=True
                        )
            
            # Save analysis to database
            analysis = models.BodyAnalysis(
                user_id=current_user.id,
                shoulder_width_ratio=result.ratios.shoulder_width_ratio,
                waist_width_ratio=result.ratios.waist_width_ratio,
                hip_width_ratio=result.ratios.hip_width_ratio,
                torso_leg_ratio=result.ratios.torso_leg_ratio,
                body_type=result.body_type,
                confidence_score=result.confidence_score,
                analysis_notes=result.notes,
                recommended_silhouettes=result.recommended_silhouettes,
                photo_front_url=photo_front_url,
                photo_side_url=photo_side_url
            )
            
            db.add(analysis)
            db.commit()
            db.refresh(analysis)
            
            return result
            
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.get("/history", response_model=list[schemas.BodyAnalysis])
async def get_analysis_history(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's body analysis history"""
    analyses = db.query(models.BodyAnalysis).filter(
        models.BodyAnalysis.user_id == current_user.id
    ).order_by(models.BodyAnalysis.created_at.desc()).all()
    
    return analyses


@router.get("/latest", response_model=schemas.BodyAnalysis)
async def get_latest_analysis(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's most recent body analysis"""
    analysis = db.query(models.BodyAnalysis).filter(
        models.BodyAnalysis.user_id == current_user.id
    ).order_by(models.BodyAnalysis.created_at.desc()).first()
    
    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="No body analysis found. Please complete a body scan first."
        )
    
    return analysis
