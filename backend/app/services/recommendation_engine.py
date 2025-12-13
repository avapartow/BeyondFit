"""
Recommendation Engine V1 - Rule-based Product Recommendations
V2 will add ML-based ranking via a pluggable interface
"""
from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from app.models import Product, BodyAnalysis, UserProfile, BodyType as ModelBodyType
from app.schemas import BodyType, RecommendationFilters, Product as ProductSchema


class RecommendationEngine:
    """Rule-based recommendation engine for clothing products"""
    
    # Mapping of body types to flattering attributes
    BODY_TYPE_ATTRIBUTES = {
        BodyType.PEAR: {
            "silhouettes": ["A-line", "fit-and-flare", "empire", "wrap"],
            "necklines": ["boat neck", "off-shoulder", "scoop", "wide"],
            "fit_types": ["fitted on top", "relaxed bottom", "structured"],
            "avoid_silhouettes": ["skinny", "pencil"],
            "preferred_categories": ["dresses", "tops", "blazers"]
        },
        BodyType.APPLE: {
            "silhouettes": ["empire", "A-line", "wrap", "shift"],
            "necklines": ["V-neck", "scoop", "sweetheart"],
            "fit_types": ["relaxed", "flowy", "tailored"],
            "lengths": ["midi", "knee-length"],
            "preferred_categories": ["dresses", "tunics", "jackets"]
        },
        BodyType.HOURGLASS: {
            "silhouettes": ["wrap", "bodycon", "fitted", "belted", "tailored"],
            "necklines": ["V-neck", "sweetheart", "scoop"],
            "fit_types": ["fitted", "tailored"],
            "rises": ["high", "mid"],
            "preferred_categories": ["dresses", "belted items", "fitted tops"]
        },
        BodyType.INVERTED_TRIANGLE: {
            "silhouettes": ["A-line", "straight", "wide-leg"],
            "necklines": ["V-neck", "scoop"],
            "fit_types": ["relaxed bottom", "structured bottom"],
            "preferred_categories": ["skirts", "dresses", "wide-leg pants"]
        },
        BodyType.RECTANGLE: {
            "silhouettes": ["wrap", "peplum", "belted", "ruffled"],
            "necklines": ["sweetheart", "ruffled", "asymmetric"],
            "fit_types": ["peplum", "layered"],
            "preferred_categories": ["dresses", "belted items", "textured pieces"]
        }
    }
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_body_type(self, user_id: int) -> Optional[BodyType]:
        """Get the most recent body type analysis for a user"""
        analysis = (
            self.db.query(BodyAnalysis)
            .filter(BodyAnalysis.user_id == user_id)
            .order_by(BodyAnalysis.created_at.desc())
            .first()
        )
        
        if analysis:
            return BodyType(analysis.body_type.value)
        return None
    
    def get_user_preferences(self, user_id: int) -> Optional[UserProfile]:
        """Get user style preferences"""
        return (
            self.db.query(UserProfile)
            .filter(UserProfile.user_id == user_id)
            .first()
        )
    
    def calculate_product_score(
        self,
        product: Product,
        body_type: BodyType,
        user_profile: Optional[UserProfile] = None,
        filters: Optional[RecommendationFilters] = None
    ) -> float:
        """
        Calculate recommendation score for a product (0-100)
        Higher score = better match
        """
        score = 50.0  # Base score
        
        # Get body type attributes
        body_attrs = self.BODY_TYPE_ATTRIBUTES.get(body_type, {})
        
        # Score based on body type suitability (most important)
        if product.suitable_for_body_types:
            body_types_list = [bt if isinstance(bt, str) else bt.value for bt in product.suitable_for_body_types]
            if body_type.value in body_types_list:
                score += 30.0
        
        # Score based on silhouette match
        if product.silhouette:
            preferred_silhouettes = body_attrs.get("silhouettes", [])
            avoid_silhouettes = body_attrs.get("avoid_silhouettes", [])
            
            silhouette_lower = product.silhouette.lower()
            if any(pref.lower() in silhouette_lower for pref in preferred_silhouettes):
                score += 15.0
            if any(avoid.lower() in silhouette_lower for avoid in avoid_silhouettes):
                score -= 20.0
        
        # Score based on neckline match
        if product.neckline:
            preferred_necklines = body_attrs.get("necklines", [])
            neckline_lower = product.neckline.lower()
            if any(pref.lower() in neckline_lower for pref in preferred_necklines):
                score += 10.0
        
        # Score based on fit type
        if product.fit_type:
            preferred_fits = body_attrs.get("fit_types", [])
            fit_lower = product.fit_type.lower()
            if any(pref.lower() in fit_lower for pref in preferred_fits):
                score += 10.0
        
        # Score based on category preference for body type
        preferred_categories = body_attrs.get("preferred_categories", [])
        if any(cat.lower() in product.category.lower() for cat in preferred_categories):
            score += 5.0
        
        # User preference scoring
        if user_profile:
            # Color preference
            if user_profile.favorite_colors and product.colors:
                if any(color in product.colors for color in user_profile.favorite_colors):
                    score += 8.0
            
            # Style preference
            if user_profile.style_preferences:
                # Map style preferences to product attributes (simplified)
                style_keywords = {
                    "minimal": ["simple", "clean", "minimal", "basic"],
                    "classic": ["classic", "timeless", "traditional"],
                    "party": ["sequin", "metallic", "embellished", "statement"],
                    "casual": ["casual", "relaxed", "everyday"],
                    "bohemian": ["boho", "flowy", "ethnic", "printed"],
                    "sporty": ["sporty", "athletic", "active"]
                }
                
                product_text = f"{product.title} {product.description}".lower()
                for style in user_profile.style_preferences:
                    keywords = style_keywords.get(style, [])
                    if any(kw in product_text for kw in keywords):
                        score += 5.0
                        break
        
        # Price filtering (hard filter, not scoring)
        if filters:
            if filters.min_price and product.price < filters.min_price:
                return 0.0
            if filters.max_price and product.price > filters.max_price:
                return 0.0
        
        # Budget preference
        if user_profile and user_profile.budget_min and user_profile.budget_max:
            if user_profile.budget_min <= product.price <= user_profile.budget_max:
                score += 5.0
        
        # Stock availability bonus
        if product.in_stock:
            score += 3.0
        
        # Sale price bonus
        if product.sale_price and product.sale_price < product.price:
            discount_percent = ((product.price - product.sale_price) / product.price) * 100
            score += min(discount_percent / 10, 5.0)  # Up to 5 points for discounts
        
        return min(max(score, 0.0), 100.0)  # Clamp between 0-100
    
    def recommend_products(
        self,
        user_id: int,
        filters: Optional[RecommendationFilters] = None,
        limit: int = 20,
        offset: int = 0
    ) -> tuple[List[Product], int, Optional[BodyType], str]:
        """
        Get personalized product recommendations
        
        Returns:
            (products, total_count, body_type, explanation)
        """
        # Get user's body type and preferences
        body_type = self.get_user_body_type(user_id)
        user_profile = self.get_user_preferences(user_id)
        
        # Build base query
        query = self.db.query(Product).filter(Product.is_active == True)
        
        # Apply filters
        if filters:
            if filters.category:
                query = query.filter(Product.category.ilike(f"%{filters.category}%"))
            
            if filters.brands:
                query = query.join(Product.brand).filter(
                    Product.brand.has(name__in=filters.brands)
                )
            
            if filters.colors:
                # Filter products that have at least one matching color
                query = query.filter(
                    Product.colors.op('&&')(filters.colors)  # PostgreSQL array overlap
                )
            
            if filters.min_price:
                query = query.filter(Product.price >= filters.min_price)
            
            if filters.max_price:
                query = query.filter(Product.price <= filters.max_price)
        
        # Get all matching products
        all_products = query.all()
        
        # Score and rank products
        if body_type:
            scored_products = [
                (product, self.calculate_product_score(product, body_type, user_profile, filters))
                for product in all_products
            ]
            # Sort by score descending
            scored_products.sort(key=lambda x: x[1], reverse=True)
            ranked_products = [p[0] for p in scored_products]
        else:
            # No body type analysis yet, use default ordering
            ranked_products = all_products
        
        total_count = len(ranked_products)
        
        # Apply pagination
        paginated_products = ranked_products[offset:offset + limit]
        
        # Generate explanation
        explanation = self._generate_explanation(body_type, user_profile, filters)
        
        return paginated_products, total_count, body_type, explanation
    
    def _generate_explanation(
        self,
        body_type: Optional[BodyType],
        user_profile: Optional[UserProfile],
        filters: Optional[RecommendationFilters]
    ) -> str:
        """Generate user-friendly explanation for recommendations"""
        parts = []
        
        if body_type:
            body_type_names = {
                BodyType.PEAR: "pear shape",
                BodyType.APPLE: "apple shape",
                BodyType.HOURGLASS: "hourglass shape",
                BodyType.INVERTED_TRIANGLE: "inverted triangle shape",
                BodyType.RECTANGLE: "rectangle shape"
            }
            parts.append(f"Curated for your {body_type_names.get(body_type, 'body type')}")
        
        if user_profile and user_profile.style_preferences:
            styles = ", ".join(user_profile.style_preferences[:2])
            parts.append(f"matching your {styles} style")
        
        if filters and filters.occasion:
            parts.append(f"perfect for {filters.occasion}")
        
        if not parts:
            return "Handpicked styles just for you"
        
        return " — ".join(parts) + "."


class RecommendationServiceInterface:
    """
    Interface for recommendation service
    V2 can implement this with ML-based ranking
    """
    
    def recommend(
        self,
        user_id: int,
        filters: Optional[RecommendationFilters] = None,
        limit: int = 20,
        offset: int = 0
    ) -> tuple[List[Product], int, Optional[BodyType], str]:
        """Get recommendations for user"""
        raise NotImplementedError


def get_recommendation_engine(db: Session) -> RecommendationEngine:
    """Factory function to get recommendation engine"""
    return RecommendationEngine(db)
