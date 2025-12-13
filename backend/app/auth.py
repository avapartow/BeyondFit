"""
Authentication utilities for JWT tokens and OTP
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import get_settings

settings = get_settings()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OTP storage (in production, use Redis)
_otp_store: dict[str, tuple[str, datetime]] = {}


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    
    return encoded_jwt


def verify_token(token: str) -> Optional[str]:
    """Verify JWT token and return email"""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email: str = payload.get("sub")
        return email
    except JWTError:
        return None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash password"""
    return pwd_context.hash(password)


def generate_otp() -> str:
    """Generate 6-digit OTP"""
    return str(secrets.randbelow(900000) + 100000)


def store_otp(email: str, otp: str, expiry_minutes: int = 10):
    """Store OTP with expiry (in production, use Redis)"""
    expiry = datetime.utcnow() + timedelta(minutes=expiry_minutes)
    _otp_store[email] = (otp, expiry)


def verify_otp(email: str, otp: str) -> bool:
    """Verify OTP code"""
    if email not in _otp_store:
        return False
    
    stored_otp, expiry = _otp_store[email]
    
    # Check if expired
    if datetime.utcnow() > expiry:
        del _otp_store[email]
        return False
    
    # Check if matches
    if stored_otp == otp:
        del _otp_store[email]  # Remove after successful verification
        return True
    
    return False


def send_otp_email(email: str, otp: str) -> bool:
    """Send OTP via email"""
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"Your BeyondFit Login Code: {otp}"
        msg['From'] = settings.from_email
        msg['To'] = email
        
        # HTML email body
        html = f"""
        <html>
          <body style="font-family: Arial, sans-serif; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: #f9f9f9; padding: 30px; border-radius: 10px;">
              <h2 style="color: #333;">Your BeyondFit Login Code</h2>
              <p style="font-size: 16px; color: #666;">
                Use this code to sign in to your BeyondFit account:
              </p>
              <div style="background: white; padding: 20px; text-align: center; border-radius: 8px; margin: 20px 0;">
                <h1 style="color: #6366f1; letter-spacing: 8px; margin: 0;">{otp}</h1>
              </div>
              <p style="font-size: 14px; color: #999;">
                This code will expire in 10 minutes.
              </p>
              <p style="font-size: 14px; color: #999;">
                If you didn't request this code, please ignore this email.
              </p>
            </div>
          </body>
        </html>
        """
        
        # Attach HTML
        msg.attach(MIMEText(html, 'html'))
        
        # Send email
        if settings.smtp_host and settings.smtp_username:
            with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
                server.starttls()
                server.login(settings.smtp_username, settings.smtp_password)
                server.send_message(msg)
            return True
        else:
            # In development, just print the OTP
            print(f"[DEV MODE] OTP for {email}: {otp}")
            return True
            
    except Exception as e:
        print(f"Error sending OTP email: {e}")
        # In development, still return True
        print(f"[DEV MODE] OTP for {email}: {otp}")
        return True
