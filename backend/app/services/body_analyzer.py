"""
Body Analysis Module using MediaPipe Pose Detection
Analyzes body photos to extract ratios and determine body type
"""
import cv2
import mediapipe as mp
import numpy as np
from typing import Dict, Tuple, Optional
from app.schemas import BodyType, BodyRatios, BodyAnalysisResult


class BodyAnalyzer:
    """Analyzes body measurements from photos using MediaPipe"""
    
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=True,
            model_complexity=2,
            enable_segmentation=False,
            min_detection_confidence=0.5
        )
        
    def analyze_photo(self, image_path: str) -> Optional[Dict]:
        """
        Analyze a single photo and extract body landmarks
        Returns landmarks dict or None if detection fails
        """
        image = cv2.imread(image_path)
        if image is None:
            return None
            
        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Process the image
        results = self.pose.process(image_rgb)
        
        if not results.pose_landmarks:
            return None
            
        # Convert landmarks to dict for easier access
        landmarks = {}
        for idx, landmark in enumerate(results.pose_landmarks.landmark):
            landmarks[idx] = {
                'x': landmark.x,
                'y': landmark.y,
                'z': landmark.z,
                'visibility': landmark.visibility
            }
            
        return landmarks
    
    def calculate_distance(self, point1: Dict, point2: Dict) -> float:
        """Calculate Euclidean distance between two landmarks"""
        dx = point2['x'] - point1['x']
        dy = point2['y'] - point1['y']
        return np.sqrt(dx**2 + dy**2)
    
    def extract_body_ratios(
        self, 
        front_landmarks: Dict,
        side_landmarks: Optional[Dict] = None
    ) -> BodyRatios:
        """
        Extract body ratios from landmarks
        
        MediaPipe Pose Landmark indices (key ones):
        11, 12: Shoulders
        23, 24: Hips
        25, 26: Knees
        27, 28: Ankles
        """
        # Shoulder width (use left and right shoulder)
        left_shoulder = front_landmarks[11]
        right_shoulder = front_landmarks[12]
        shoulder_width = self.calculate_distance(left_shoulder, right_shoulder)
        
        # Hip width
        left_hip = front_landmarks[23]
        right_hip = front_landmarks[24]
        hip_width = self.calculate_distance(left_hip, right_hip)
        
        # Waist approximation (midpoint between shoulders and hips)
        # For waist, we estimate based on shoulder/hip ratio
        # This is a simplified approach - real waist measurement would need more sophisticated detection
        waist_width = (shoulder_width + hip_width) / 2.5  # Approximation
        
        # Torso length (shoulder to hip)
        torso_length = self.calculate_distance(left_shoulder, left_hip)
        
        # Leg length (hip to ankle)
        left_ankle = front_landmarks[27]
        leg_length = self.calculate_distance(left_hip, left_ankle)
        
        # Calculate ratios (normalized)
        # Use hip width as base for normalization
        base = hip_width if hip_width > 0 else 1.0
        
        shoulder_ratio = shoulder_width / base
        waist_ratio = waist_width / base
        hip_ratio = 1.0  # Hip is the base
        torso_leg_ratio = torso_length / leg_length if leg_length > 0 else 1.0
        
        return BodyRatios(
            shoulder_width_ratio=round(shoulder_ratio, 3),
            waist_width_ratio=round(waist_ratio, 3),
            hip_width_ratio=round(hip_ratio, 3),
            torso_leg_ratio=round(torso_leg_ratio, 3)
        )
    
    def classify_body_type(self, ratios: BodyRatios) -> Tuple[BodyType, float, str]:
        """
        Classify body type based on ratios
        Returns: (body_type, confidence_score, explanation)
        """
        shoulder = ratios.shoulder_width_ratio
        waist = ratios.waist_width_ratio
        hip = ratios.hip_width_ratio  # Always 1.0 as base
        
        # Classification rules with confidence scoring
        confidence = 0.0
        body_type = BodyType.RECTANGLE
        explanation = ""
        
        # Rule-based classification
        if shoulder > 1.05 and waist < 0.85:
            # Shoulders notably wider than hips, defined waist
            body_type = BodyType.INVERTED_TRIANGLE
            confidence = min(0.9, 0.6 + (shoulder - 1.05) * 2)
            explanation = "Broader shoulders with narrower hips and defined waist"
            
        elif hip > shoulder * 1.05 and waist < 0.85:
            # Hips wider than shoulders, defined waist
            body_type = BodyType.PEAR
            confidence = min(0.9, 0.6 + (hip - shoulder * 1.05) * 2)
            explanation = "Narrower shoulders with fuller hips and defined waist"
            
        elif abs(shoulder - hip) <= 0.05 and waist < 0.8:
            # Shoulders and hips similar, small waist
            body_type = BodyType.HOURGLASS
            confidence = min(0.9, 0.7 + (0.8 - waist) * 2)
            explanation = "Balanced shoulders and hips with a well-defined waist"
            
        elif abs(shoulder - hip) <= 0.05 and waist >= 0.8:
            # Shoulders and hips similar, less defined waist
            body_type = BodyType.RECTANGLE
            confidence = min(0.85, 0.65 + (waist - 0.8) * 1.5)
            explanation = "Balanced proportions with a straighter silhouette"
            
        elif waist > 0.9 and shoulder > hip:
            # Fuller midsection
            body_type = BodyType.APPLE
            confidence = min(0.85, 0.6 + (waist - 0.9) * 2)
            explanation = "Fuller midsection with weight carried around the waist"
            
        else:
            # Default to rectangle with lower confidence
            body_type = BodyType.RECTANGLE
            confidence = 0.5
            explanation = "Relatively balanced proportions"
        
        return body_type, round(confidence, 2), explanation
    
    def get_recommended_silhouettes(self, body_type: BodyType) -> list[str]:
        """Get recommended clothing silhouettes for each body type"""
        
        recommendations = {
            BodyType.PEAR: [
                "A-line skirts and dresses",
                "Boat neck and off-shoulder tops",
                "Structured shoulders",
                "Dark bottom, bright top combinations",
                "Wide-leg pants",
                "Fit-and-flare dresses"
            ],
            BodyType.APPLE: [
                "Empire waist dresses",
                "V-neck and scoop neck tops",
                "A-line silhouettes",
                "Mid-rise bottoms",
                "Longer tops that skim the body",
                "Wrap dresses"
            ],
            BodyType.HOURGLASS: [
                "Wrap dresses and tops",
                "Belted styles",
                "Fitted silhouettes",
                "High-waisted bottoms",
                "Tailored pieces",
                "Bodycon dresses"
            ],
            BodyType.INVERTED_TRIANGLE: [
                "A-line skirts and dresses",
                "Straight-leg or wide-leg pants",
                "V-neck tops",
                "Darker colors on top",
                "Full or pleated skirts",
                "Bootcut jeans"
            ],
            BodyType.RECTANGLE: [
                "Belted dresses and tops",
                "Peplum styles",
                "Ruffles and embellishments",
                "Curved seams and details",
                "Wrap styles",
                "Layered looks"
            ]
        }
        
        return recommendations.get(body_type, [])
    
    def analyze_body(
        self, 
        front_photo_path: str, 
        side_photo_path: Optional[str] = None
    ) -> BodyAnalysisResult:
        """
        Complete body analysis from photos
        
        Args:
            front_photo_path: Path to front-facing photo
            side_photo_path: Optional path to side-facing photo
            
        Returns:
            BodyAnalysisResult with type, ratios, and recommendations
            
        Raises:
            ValueError: If landmark detection fails
        """
        # Analyze front photo
        front_landmarks = self.analyze_photo(front_photo_path)
        if not front_landmarks:
            raise ValueError("Could not detect body landmarks in front photo. Please ensure good lighting and full body visibility.")
        
        # Analyze side photo if provided
        side_landmarks = None
        if side_photo_path:
            side_landmarks = self.analyze_photo(side_photo_path)
        
        # Extract ratios
        ratios = self.extract_body_ratios(front_landmarks, side_landmarks)
        
        # Classify body type
        body_type, confidence, explanation = self.classify_body_type(ratios)
        
        # Get recommendations
        silhouettes = self.get_recommended_silhouettes(body_type)
        
        return BodyAnalysisResult(
            body_type=body_type,
            confidence_score=confidence,
            ratios=ratios,
            notes=explanation,
            recommended_silhouettes=silhouettes
        )
    
    def __del__(self):
        """Cleanup MediaPipe resources"""
        if hasattr(self, 'pose'):
            self.pose.close()


# Singleton instance
_analyzer_instance = None

def get_body_analyzer() -> BodyAnalyzer:
    """Get or create BodyAnalyzer singleton"""
    global _analyzer_instance
    if _analyzer_instance is None:
        _analyzer_instance = BodyAnalyzer()
    return _analyzer_instance
