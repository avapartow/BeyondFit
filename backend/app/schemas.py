from pydantic import BaseModel, EmailStr, Field, HttpUrl
from typing import Optional, List
from datetime import datetime
from enum import Enum


# Enums
class BodyType(str, Enum):
    PEAR = "pear"
    APPLE = "apple"
    RECTANGLE = "rectangle"
    HOURGLASS = "hourglass"
    INVERTED_TRIANGLE = "inverted_triangle"


class StylePreference(str, Enum):
    MINIMAL = "minimal"
    CLASSIC = "classic"
    PARTY = "party"
    CASUAL = "casual"
    BOHEMIAN = "bohemian"
    SPORTY = "sporty"


# User Schemas
class UserProfileCreate(BaseModel):
    style_preferences: List[StylePreference]
    budget_min: float = Field(ge=0)
    budget_max: float = Field(ge=0)
    region: str
    favorite_colors: List[str] = []
    size_top: Optional[str] = None
    size_bottom: Optional[str] = None
    size_dress: Optional[str] = None
    size_shoes: Optional[str] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    store_photos: bool = False


class UserProfileUpdate(BaseModel):
    style_preferences: Optional[List[StylePreference]] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    region: Optional[str] = None
    favorite_colors: Optional[List[str]] = None
    size_top: Optional[str] = None
    size_bottom: Optional[str] = None
    size_dress: Optional[str] = None
    size_shoes: Optional[str] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    store_photos: Optional[bool] = None


class UserProfile(BaseModel):
    id: int
    user_id: int
    style_preferences: List[str]
    budget_min: Optional[float]
    budget_max: Optional[float]
    region: Optional[str]
    favorite_colors: List[str]
    size_top: Optional[str]
    size_bottom: Optional[str]
    size_dress: Optional[str]
    size_shoes: Optional[str]
    height_cm: Optional[float]
    weight_kg: Optional[float]
    store_photos: bool
    
    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr


class User(BaseModel):
    id: int
    email: str
    created_at: datetime
    is_active: bool
    profile: Optional[UserProfile] = None
    
    class Config:
        from_attributes = True


# Body Analysis Schemas
class BodyRatios(BaseModel):
    shoulder_width_ratio: float
    waist_width_ratio: float
    hip_width_ratio: float
    torso_leg_ratio: float


class BodyAnalysisResult(BaseModel):
    body_type: BodyType
    confidence_score: float = Field(ge=0.0, le=1.0)
    ratios: BodyRatios
    notes: str
    recommended_silhouettes: List[str]


class BodyAnalysis(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    shoulder_width_ratio: float
    waist_width_ratio: float
    hip_width_ratio: float
    torso_leg_ratio: float
    body_type: str
    confidence_score: float
    analysis_notes: str
    recommended_silhouettes: List[str]
    
    class Config:
        from_attributes = True


# Product Schemas
class ProductCreate(BaseModel):
    product_id: str
    brand_id: int
    title: str
    description: str
    category: str
    subcategory: Optional[str] = None
    price: float
    sale_price: Optional[float] = None
    currency: str = "USD"
    available_sizes: List[str]
    in_stock: bool = True
    fit_type: str
    silhouette: str
    neckline: Optional[str] = None
    sleeve_length: Optional[str] = None
    length: Optional[str] = None
    rise: Optional[str] = None
    material: Optional[str] = None
    colors: List[str]
    suitable_for_body_types: List[BodyType] = []
    image_url: str
    affiliate_url: str


class ProductUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    sale_price: Optional[float] = None
    in_stock: Optional[bool] = None
    available_sizes: Optional[List[str]] = None
    is_active: Optional[bool] = None


class Product(BaseModel):
    id: int
    brand_id: int
    product_id: str
    title: str
    description: str
    category: str
    subcategory: Optional[str]
    price: float
    sale_price: Optional[float]
    currency: str
    available_sizes: List[str]
    in_stock: bool
    fit_type: str
    silhouette: str
    neckline: Optional[str]
    sleeve_length: Optional[str]
    length: Optional[str]
    rise: Optional[str]
    material: Optional[str]
    colors: List[str]
    suitable_for_body_types: List[str]
    image_url: str
    affiliate_url: str
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True


# Brand Schemas
class BrandCreate(BaseModel):
    name: str
    logo_url: Optional[str] = None
    description: Optional[str] = None
    website_url: str
    affiliate_network: str
    affiliate_id: str
    commission_rate: float = Field(ge=0.0, le=100.0)


class BrandUpdate(BaseModel):
    name: Optional[str] = None
    logo_url: Optional[str] = None
    description: Optional[str] = None
    website_url: Optional[str] = None
    commission_rate: Optional[float] = None
    is_active: Optional[bool] = None


class Brand(BaseModel):
    id: int
    name: str
    logo_url: Optional[str]
    description: Optional[str]
    website_url: str
    affiliate_network: str
    affiliate_id: str
    commission_rate: float
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True


# Recommendation Schemas
class RecommendationFilters(BaseModel):
    occasion: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    colors: Optional[List[str]] = None
    brands: Optional[List[str]] = None
    category: Optional[str] = None
    size: Optional[str] = None


class RecommendationResponse(BaseModel):
    products: List[Product]
    total_count: int
    body_type: Optional[BodyType] = None
    explanation: str


# Lookbook Schemas
class LookbookCreate(BaseModel):
    name: str
    description: Optional[str] = None
    product_ids: List[int] = []


class Lookbook(BaseModel):
    id: int
    user_id: int
    name: str
    description: Optional[str]
    product_ids: List[int]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# Analytics Schemas
class AffiliateClickCreate(BaseModel):
    product_id: int
    user_id: Optional[int] = None
    ip_address: str
    user_agent: str
    referrer: Optional[str] = None


class AnalyticsOverview(BaseModel):
    total_clicks: int
    total_conversions: int
    conversion_rate: float
    total_commission_earned: float
    top_products: List[dict]
    top_categories: List[dict]


# Auth Schemas
class OTPRequest(BaseModel):
    email: EmailStr


class OTPVerify(BaseModel):
    email: EmailStr
    otp_code: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


# Admin Schemas
class AdminLogin(BaseModel):
    email: EmailStr
    password: str


class ProductCSVUpload(BaseModel):
    brand_id: int
