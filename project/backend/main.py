from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import pickle
import re
import os
from datetime import datetime

app = FastAPI(title="AI-PhishGuard Hybrid API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

try:
    with open(os.path.join(MODEL_DIR, 'scaler.pkl'), 'rb') as f:
        scaler = pickle.load(f)
    with open(os.path.join(MODEL_DIR, 'autoencoder.pkl'), 'rb') as f:
        autoencoder = pickle.load(f)
    with open(os.path.join(MODEL_DIR, 'random_forest.pkl'), 'rb') as f:
        rf_model = pickle.load(f)
    with open(os.path.join(MODEL_DIR, 'config.pkl'), 'rb') as f:
        model_config = pickle.load(f)
    
    print("✓ All models loaded successfully")
    print(f"✓ Features: {len(model_config.get('autoencoder_features', []))}")
    
except Exception as e:
    print(f"⚠ Error loading models: {e}")
    print("Please run: python train_model.py")

class EmailInput(BaseModel):
    subject: str
    body: str
    sender: str
    receiver: str

class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
    reconstruction_error: float
    is_phishing: bool
    risk_level: str
    explanation: str
    ml_confidence: float = 0.0
    rule_based_adjustment: float = 0.0
    detection_method: str = "unknown"

def extract_features(subject: str, body: str, sender: str, receiver: str) -> np.ndarray:
    """Extract features EXACTLY as in training"""
    
    subject = str(subject).strip()
    body = str(body).strip()
    sender = str(sender).strip()
    receiver = str(receiver).strip()
    
    phishing_keywords = model_config['phishing_keywords']
    
    features = {}
    
    # Basic length features
    features['subject_length'] = len(subject)
    features['body_length'] = len(body)
    features['sender_length'] = len(sender)
    
    # URL features
    features['has_url'] = int(bool(re.search(r'http[s]?://', body)))
    features['url_count'] = len(re.findall(r'http[s]?://', body))
    features['suspicious_url'] = int(bool(re.search(r'(bit\.ly|goo\.gl|tinyurl|click|redirect)', body, re.IGNORECASE)))
    
    # Character ratio features
    features['special_char_ratio'] = len(re.findall(r'[^\w\s]', body)) / max(len(body), 1)
    features['digit_ratio'] = len(re.findall(r'\d', body)) / max(len(body), 1)
    features['uppercase_ratio'] = len(re.findall(r'[A-Z]', body)) / max(len(body), 1)
    
    # Word features
    words = body.split()
    features['word_count'] = len(words)
    features['avg_word_length'] = np.mean([len(w) for w in words]) if words else 0
    features['subject_word_count'] = len(subject.split())
    
    # Keyword features
    for word in phishing_keywords:
        features[f'has_{word}'] = int(word.lower() in (body.lower() + " " + subject.lower()))
    
    # Sender features
    features['suspicious_sender'] = int(bool(
        re.search(r'[\d]{5,}', sender) or
        re.search(r'[!$%^&*()_+\-=\[\]{};\':"\\|,.<>/?]', sender)
    ))
    
    # Greeting features
    features['generic_greeting'] = int(bool(re.search(r'^(dear|customer|user|valued)', body, re.IGNORECASE)))
    
    # Time features
    now = datetime.now()
    features['hour'] = now.hour
    features['day_of_week'] = now.weekday()
    
    # Build feature vector
    feature_order = model_config['autoencoder_features']
    feature_vector = []
    
    for f in feature_order:
        feature_vector.append(features.get(f, 0))
    
    return np.array(feature_vector)

class RuleBasedDetector:
    """Rule-based component for obvious cases"""
    
    @staticmethod
    def analyze_email(subject: str, body: str, sender: str) -> dict:
        """Analyze email using rule-based logic"""
        
        body_lower = body.lower()
        subject_lower = subject.lower()
        combined_text = f"{subject_lower} {body_lower}"
        
        # Rule 1: Check for obvious phishing patterns
        strong_phishing_indicators = {
            'has_suspicious_url': bool(re.search(r'(bit\.ly|goo\.gl|tinyurl|click|redirect)', body_lower, re.IGNORECASE)),
            'has_http_url': bool(re.search(r'http[s]?://', body_lower)),
            'has_urgent_keywords': bool(re.search(r'\b(urgent|immediate|verify now|action required|account suspended|password expired)\b', combined_text, re.IGNORECASE)),
            'has_payment_demands': bool(re.search(r'\b(pay|payment|send money|transfer|rs |\$|₹)\b.*\b(now|immediately|urgent)\b', combined_text, re.IGNORECASE)),
            'suspicious_sender_format': bool(re.search(r'[\d]{8,}|[!$%^&*()_+\-=\[\]{};\':"\\|,.<>/?]{3,}', sender)),
        }
        
        # Rule 2: Check for obvious legitimate patterns
        strong_legitimate_indicators = {
            'very_short_simple': len(body) < 30 and len(subject) < 15 and not re.search(r'http[s]?://', body),
            'personal_conversation': bool(re.search(r'^(hi|hello|hey|dear [a-z]|greetings)', body_lower, re.IGNORECASE)) and not re.search(r'\b(urgent|verify|account|payment)\b', combined_text, re.IGNORECASE),
            'normal_sender': bool(re.search(r'@(gmail\.com|yahoo\.com|outlook\.com|hotmail\.com)$', sender.lower())),
            'work_related': bool(re.search(r'\b(meeting|reminder|team|project|update|schedule)\b', combined_text, re.IGNORECASE)) and not re.search(r'\b(urgent|verify|account)\b', combined_text, re.IGNORECASE),
        }
        
        phishing_score = sum(strong_phishing_indicators.values())
        legitimate_score = sum(strong_legitimate_indicators.values())
        
        return {
            'phishing_indicators': strong_phishing_indicators,
            'legitimate_indicators': strong_legitimate_indicators,
            'phishing_score': phishing_score,
            'legitimate_score': legitimate_score,
            'certain_phishing': phishing_score >= 2,
            'certain_legitimate': legitimate_score >= 2 and phishing_score == 0
        }

class HybridDetector:
    """Hybrid detector that combines ML and rule-based logic"""
    
    def __init__(self, ml_model, scaler, autoencoder, config):
        self.ml_model = ml_model
        self.scaler = scaler
        self.autoencoder = autoencoder
        self.config = config
        self.rule_detector = RuleBasedDetector()
        
    def detect(self, subject: str, body: str, sender: str, receiver: str) -> dict:
        """Hybrid detection combining ML and rules"""
        
        # Step 1: Rule-based analysis for obvious cases
        rule_analysis = self.rule_detector.analyze_email(subject, body, sender)
        
        # If rule-based detection is certain, use it
        if rule_analysis['certain_phishing']:
            return {
                'prediction': 'phishing',
                'confidence': 0.95,
                'is_phishing': True,
                'method': 'rule_based',
                'reason': 'Multiple strong phishing indicators detected',
                'ml_probability': 0.0,  # Use 0.0 instead of None
                'rule_adjustment': 0.45,  # Strong adjustment toward phishing
                'reconstruction_error': 0.0
            }
        
        if rule_analysis['certain_legitimate']:
            return {
                'prediction': 'legitimate',
                'confidence': 0.90,
                'is_phishing': False,
                'method': 'rule_based',
                'reason': 'Multiple strong legitimate indicators with no phishing signs',
                'ml_probability': 0.0,  # Use 0.0 instead of None
                'rule_adjustment': -0.40,  # Strong adjustment toward legitimate
                'reconstruction_error': 0.0
            }
        
        # Step 2: ML prediction for ambiguous cases
        features = extract_features(subject, body, sender, receiver)
        features_scaled = self.scaler.transform([features])[0]
        
        # Get reconstruction error
        autoencoder_reconstruction = self.autoencoder.predict([features_scaled])[0]
        reconstruction_error = np.mean((features_scaled - autoencoder_reconstruction) ** 2)
        
        # Create enhanced features
        features_enhanced = np.concatenate([
            features_scaled,
            [reconstruction_error],
            [reconstruction_error ** 2],
            [np.sqrt(reconstruction_error)]
        ])
        
        # Get ML probabilities
        ml_proba = self.ml_model.predict_proba([features_enhanced])[0]
        ml_phishing_prob = float(ml_proba[1])
        ml_legitimate_prob = float(ml_proba[0])
        
        # Step 3: Apply rule-based adjustments to ML probability
        adjusted_prob = self._apply_rule_adjustments(ml_phishing_prob, rule_analysis)
        
        # Step 4: Make final decision
        is_phishing = adjusted_prob > 0.5
        final_confidence = adjusted_prob if is_phishing else (1 - adjusted_prob)
        
        # Determine which method contributed more
        ml_contribution = abs(ml_phishing_prob - 0.5)
        rule_contribution = abs(adjusted_prob - ml_phishing_prob)
        
        if rule_contribution > ml_contribution * 0.5:
            method = 'hybrid_rules_dominant'
        else:
            method = 'hybrid_ml_dominant'
        
        return {
            'prediction': 'phishing' if is_phishing else 'legitimate',
            'confidence': final_confidence,
            'is_phishing': is_phishing,
            'method': method,
            'reason': 'Combined ML and rule-based analysis',
            'ml_probability': ml_phishing_prob,
            'rule_adjustment': adjusted_prob - ml_phishing_prob,
            'reconstruction_error': reconstruction_error,
            'rule_analysis': rule_analysis
        }
    
    def _apply_rule_adjustments(self, ml_prob: float, rule_analysis: dict) -> float:
        """Apply rule-based adjustments to ML probability"""
        
        adjustment = 0.0
        
        # Rule adjustments (positive = more phishing, negative = more legitimate)
        
        # Strong phishing indicators increase probability
        if rule_analysis['phishing_score'] >= 3:
            adjustment += 0.25
        elif rule_analysis['phishing_score'] >= 2:
            adjustment += 0.15
        elif rule_analysis['phishing_score'] >= 1:
            adjustment += 0.08
        
        # Strong legitimate indicators decrease probability
        if rule_analysis['legitimate_score'] >= 3:
            adjustment -= 0.20
        elif rule_analysis['legitimate_score'] >= 2:
            adjustment -= 0.12
        elif rule_analysis['legitimate_score'] >= 1:
            adjustment -= 0.06
        
        # Specific rule: Very short emails are less likely to be phishing
        if rule_analysis['legitimate_indicators'].get('very_short_simple', False):
            adjustment -= 0.10
        
        # Apply adjustment with bounds
        adjusted_prob = ml_prob + adjustment
        adjusted_prob = max(0.05, min(0.95, adjusted_prob))  # Keep within reasonable bounds
        
        return adjusted_prob

def generate_explanation(result: dict) -> str:
    """Generate explanation based on hybrid detection result"""
    
    if result['method'] == 'rule_based':
        return f"Rule-based detection: {result['reason']}. Confidence: {result['confidence']:.1%}."
    
    ml_prob = result.get('ml_probability', 0.0)
    adjustment = result.get('rule_adjustment', 0)
    
    if result['is_phishing']:
        if result['confidence'] > 0.85:
            return f"High-confidence phishing detection ({result['confidence']:.1%}). ML predicted {ml_prob:.1%} probability, rules added {adjustment:+.2f} adjustment."
        elif result['confidence'] > 0.75:
            return f"Likely phishing email ({result['confidence']:.1%}). ML predicted {ml_prob:.1%} probability."
        else:
            return f"Suspicious email ({result['confidence']:.1%}). Mixed signals detected."
    else:
        if result['confidence'] > 0.90:
            return f"Very likely legitimate ({result['confidence']:.1%}). ML predicted {1-ml_prob:.1%} probability, rules added {adjustment:+.2f} adjustment."
        elif result['confidence'] > 0.80:
            return f"Likely legitimate ({result['confidence']:.1%}). Minimal risk factors."
        else:
            return f"Probably legitimate ({result['confidence']:.1%}). Some uncertainty remains."

# Initialize hybrid detector
hybrid_detector = HybridDetector(rf_model, scaler, autoencoder, model_config)

@app.get("/")
async def root():
    return {
        "message": "AI-PhishGuard Hybrid API",
        "version": "1.0.0",
        "endpoint": "/predict",
        "detection_method": "Hybrid (ML + Rule-based)",
        "status": "ready"
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict(email: EmailInput):
    """Hybrid prediction combining ML and rule-based logic"""
    
    try:
        print(f"\n{'='*60}")
        print(f"🤖 HYBRID DETECTION - Processing email")
        print(f"Subject: {email.subject}")
        print(f"Body: {len(email.body)} chars")
        print(f"Sender: {email.sender}")
        
        # Use hybrid detector
        result = hybrid_detector.detect(
            email.subject, email.body, email.sender, email.receiver
        )
        
        # Determine risk level
        if result['is_phishing']:
            if result['confidence'] > 0.85:
                risk_level = "CRITICAL"
            elif result['confidence'] > 0.75:
                risk_level = "HIGH"
            elif result['confidence'] > 0.65:
                risk_level = "MEDIUM"
            else:
                risk_level = "LOW"
        else:
            if result['confidence'] > 0.95:
                risk_level = "SAFE"
            elif result['confidence'] > 0.85:
                risk_level = "LOW"
            elif result['confidence'] > 0.75:
                risk_level = "MEDIUM"
            else:
                risk_level = "UNCERTAIN"
        
        explanation = generate_explanation(result)
        
        print(f"📊 ML Probability: {result.get('ml_probability', 0.0):.3f}")
        print(f"📈 Rule Adjustment: {result.get('rule_adjustment', 0):+.3f}")
        print(f"🎯 Final Confidence: {result['confidence']:.2%}")
        print(f"✅ Prediction: {result['prediction'].upper()} ({result['method']})")
        print(f"⚠️  Risk Level: {risk_level}")
        print(f"📝 Explanation: {explanation}")
        print(f"{'='*60}\n")
        
        # FIXED: Handle ml_probability safely
        ml_confidence = result.get('ml_probability')
        if ml_confidence is None:
            ml_confidence = result['confidence']  # Use final confidence if ML wasn't used
        
        return PredictionResponse(
            prediction=result['prediction'],
            confidence=result['confidence'],
            reconstruction_error=float(result.get('reconstruction_error', 0)),
            is_phishing=result['is_phishing'],
            risk_level=risk_level,
            explanation=explanation,
            ml_confidence=float(ml_confidence),
            rule_based_adjustment=float(result.get('rule_adjustment', 0)),
            detection_method=result['method']
        )
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.post("/analyze_detection")
async def analyze_detection(email: EmailInput):
    """Detailed analysis of detection process"""
    
    result = hybrid_detector.detect(
        email.subject, email.body, email.sender, email.receiver
    )
    
    return {
        "email_info": {
            "subject": email.subject,
            "body_length": len(email.body),
            "sender": email.sender
        },
        "detection_result": {
            "prediction": result['prediction'],
            "confidence": result['confidence'],
            "method": result['method']
        },
        "ml_component": {
            "probability": result.get('ml_probability'),
            "contribution": "Used" if result.get('ml_probability', 0) > 0 else "Not used (rule-based decision)"
        },
        "rule_component": {
            "phishing_indicators": result.get('rule_analysis', {}).get('phishing_indicators', {}),
            "legitimate_indicators": result.get('rule_analysis', {}).get('legitimate_indicators', {}),
            "phishing_score": result.get('rule_analysis', {}).get('phishing_score', 0),
            "legitimate_score": result.get('rule_analysis', {}).get('legitimate_score', 0),
            "adjustment_applied": result.get('rule_adjustment', 0)
        },
        "explanation": result.get('reason', '')
    }

@app.post("/test_scenarios")
async def test_scenarios():
    """Test various email scenarios"""
    
    test_cases = [
        {
            "name": "1. Obvious Phishing",
            "email": EmailInput(
                subject="URGENT: Verify Your Bank Account NOW",
                body="Dear customer, your account will be suspended. Click http://bit.ly/fake-bank-login to verify immediately.",
                sender="security@bank12345!!.com",
                receiver="user@gmail.com"
            )
        },
        {
            "name": "2. Normal Conversation",
            "email": EmailInput(
                subject="Meeting tomorrow",
                body="Hi team, don't forget our 2pm meeting tomorrow in conference room B.",
                sender="manager@company.com",
                receiver="team@company.com"
            )
        },
        {
            "name": "3. Short Casual",
            "email": EmailInput(
                subject="hi",
                body="hello, how are you?",
                sender="friend@gmail.com",
                receiver="me@gmail.com"
            )
        },
        {
            "name": "4. Suspicious Payment",
            "email": EmailInput(
                subject="Pay 1000 Rs urgently",
                body="You need to pay immediately. Send money to this account.",
                sender="payment@urgent123.com",
                receiver="user@gmail.com"
            )
        },
        {
            "name": "5. Class Cancellation",
            "email": EmailInput(
                subject="Class cancelled",
                body="Today's class is cancelled due to weather conditions.",
                sender="professor@university.edu",
                receiver="students@university.edu"
            )
        }
    ]
    
    results = []
    for test in test_cases:
        print(f"\n🧪 Testing: {test['name']}")
        try:
            result = await predict(test["email"])
            results.append({
                "scenario": test["name"],
                "prediction": result.prediction,
                "is_phishing": result.is_phishing,
                "confidence": result.confidence,
                "risk_level": result.risk_level,
                "detection_method": result.detection_method,
                "ml_confidence": result.ml_confidence
            })
        except Exception as e:
            results.append({
                "scenario": test["name"],
                "error": str(e)
            })
    
    return {
        "message": "Hybrid model test results",
        "results": results,
        "summary": {
            "total": len(results),
            "phishing_detected": sum(1 for r in results if isinstance(r, dict) and r.get("is_phishing", False)),
            "legitimate_detected": sum(1 for r in results if isinstance(r, dict) and not r.get("is_phishing", True)),
            "rule_based_decisions": sum(1 for r in results if isinstance(r, dict) and "rule_based" in r.get("detection_method", "")),
            "ml_based_decisions": sum(1 for r in results if isinstance(r, dict) and "ml" in r.get("detection_method", ""))
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "models_loaded": True,
        "detection_type": "hybrid",
        "components": ["rule_based", "ml_random_forest", "autoencoder"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")