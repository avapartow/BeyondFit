from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, JSON, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class BodyType(str, enum.Enum):
    PEAR = "pear"
    APPLE = "apple"
    RECTANGLE = "rectangle"
    HOURGLASS = "hourglass"
    INVERTED_TRIANGLE = "inverted_triangle"


class StylePreference(str, enum.Enum):
    MINIMAL = "minimal"
    CLASSIC = "classic"
    PARTY = "party"
    CASUAL = "casual"
    BOHEMIAN = "bohemian"
    SPORTY = "sporty"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Auth
    auth_provider = Column(String, default="email")  # email, google, apple
    is_active = Column(Boolean, default=True)
    
    # Profile
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    body_analysis = relationship("BodyAnalysis", back_populates="user")
    favorites = relationship("Favorite", back_populates="user")
    lookbooks = relationship("Lookbook", back_populates="user")


class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    
    # Preferences
    style_preferences = Column(JSON)  # List of StylePreference
    budget_min = Column(Float)
    budget_max = Column(Float)
    region = Column(String)
    favorite_colors = Column(JSON)  # List of color strings
    
    # Sizes
    size_top = Column(String)
    size_bottom = Column(String)
    size_dress = Column(String)
    size_shoes = Column(String)
    
    # Measurements (optional)
    height_cm = Column(Float, nullable=True)
    weight_kg = Column(Float, nullable=True)
    
    # Privacy
    store_photos = Column(Boolean, default=False)
    
    user = relationship("User", back_populates="profile")


class BodyAnalysis(Base):
    __tablename__ = "body_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Body ratios (derived from photos)
    shoulder_width_ratio = Column(Float)
    waist_width_ratio = Column(Float)
    hip_width_ratio = Column(Float)
    torso_leg_ratio = Column(Float)
    
    # Classification
    body_type = Column(Enum(BodyType))
    confidence_score = Column(Float)
    
    # Metadata
    analysis_notes = Column(Text)
    recommended_silhouettes = Column(JSON)  # List of recommended styles
    
    # Photo references (only if user opted in)
    photo_front_url = Column(String, nullable=True)
    photo_side_url = Column(String, nullable=True)
    
    user = relationship("User", back_populates="body_analysis")


class Brand(Base):
    __tablename__ = "brands"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    logo_url = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    website_url = Column(String)
    
    # Affiliate
    affiliate_network = Column(String)  # e.g., "ShareASale", "Impact", "Custom"
    affiliate_id = Column(String)
    commission_rate = Column(Float)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    
    products = relationship("Product", back_populates="brand")


class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"))
    
    # Basic info
    product_id = Column(String, unique=True, index=True)  # External product ID
    title = Column(String)
    description = Column(Text)
    category = Column(String)  # tops, bottoms, dresses, outerwear, etc.
    subcategory = Column(String, nullable=True)  # blouse, jeans, midi-dress, etc.
    
    # Pricing
    price = Column(Float)
    sale_price = Column(Float, nullable=True)
    currency = Column(String, default="USD")
    
    # Availability
    available_sizes = Column(JSON)  # List of sizes
    in_stock = Column(Boolean, default=True)
    
    # Attributes for recommendations
    fit_type = Column(String)  # fitted, relaxed, oversized, tailored
    silhouette = Column(String)  # A-line, wrap, straight, etc.
    neckline = Column(String, nullable=True)  # V-neck, crew, scoop, etc.
    sleeve_length = Column(String, nullable=True)  # short, long, sleeveless
    length = Column(String, nullable=True)  # mini, midi, maxi, cropped, etc.
    rise = Column(String, nullable=True)  # high, mid, low (for bottoms)
    material = Column(String, nullable=True)
    colors = Column(JSON)  # Available colors
    
    # Body type suitability (computed or manual)
    suitable_for_body_types = Column(JSON)  # List of BodyType
    
    # Links
    image_url = Column(String)
    affiliate_url = Column(String)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    
    brand = relationship("Brand", back_populates="products")


class Favorite(Base):
    __tablename__ = "favorites"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="favorites")


class Lookbook(Base):
    __tablename__ = "lookbooks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    description = Column(Text, nullable=True)
    product_ids = Column(JSON)  # List of product IDs
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("User", back_populates="lookbooks")


class AffiliateClick(Base):
    __tablename__ = "affiliate_clicks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    
    # Tracking
    clicked_at = Column(DateTime(timezone=True), server_default=func.now())
    ip_address = Column(String)
    user_agent = Column(String)
    referrer = Column(String, nullable=True)
    
    # Conversion (if webhook returns data)
    converted = Column(Boolean, default=False)
    conversion_date = Column(DateTime(timezone=True), nullable=True)
    commission_earned = Column(Float, nullable=True)


class AdminUser(Base):
    __tablename__ = "admin_users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
