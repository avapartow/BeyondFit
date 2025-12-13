from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas, auth
from datetime import timedelta

router = APIRouter()


@router.post("/request-otp", response_model=dict)
async def request_otp(request: schemas.OTPRequest, db: Session = Depends(get_db)):
    """
    Request OTP code via email
    Creates user if doesn't exist
    """
    # Check if user exists
    user = db.query(models.User).filter(models.User.email == request.email).first()
    
    if not user:
        # Create new user
        user = models.User(email=request.email, auth_provider="email")
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # Generate and send OTP
    otp = auth.generate_otp()
    auth.store_otp(request.email, otp)
    
    # Send email
    sent = auth.send_otp_email(request.email, otp)
    
    if not sent:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send OTP email"
        )
    
    return {"message": "OTP sent to your email"}


@router.post("/verify-otp", response_model=schemas.Token)
async def verify_otp(request: schemas.OTPVerify, db: Session = Depends(get_db)):
    """Verify OTP and return access token"""
    # Verify OTP
    if not auth.verify_otp(request.email, request.otp_code):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired OTP code"
        )
    
    # Get user
    user = db.query(models.User).filter(models.User.email == request.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Create access token
    access_token = auth.create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=30)
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/admin/login", response_model=schemas.Token)
async def admin_login(request: schemas.AdminLogin, db: Session = Depends(get_db)):
    """Admin login with email/password"""
    admin = db.query(models.AdminUser).filter(models.AdminUser.email == request.email).first()
    
    if not admin or not auth.verify_password(request.password, admin.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Create access token
    access_token = auth.create_access_token(
        data={"sub": admin.email, "role": "admin"}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
