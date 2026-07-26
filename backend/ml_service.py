from pathlib import Path
import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent

MODEL_DIR = ROOT / "models"

model = joblib.load(MODEL_DIR / "random_forest.pkl")
encoder = joblib.load(MODEL_DIR / "label_encoder.pkl")
feature_names = joblib.load(MODEL_DIR / "feature_names.pkl")


def predict_attack(features: dict):

    df = pd.DataFrame([features])

    # Keep columns in the same order as training
    df = df[feature_names]

    prediction = model.predict(df)[0]
    confidence = model.predict_proba(df).max() * 100

    attack = encoder.inverse_transform([prediction])[0]

    # Threat Level Mapping
    high = [
        "DDoS-TCP_Flood",
        "DDoS-UDP_Flood",
        "DDoS-SYN_Flood",
        "DDoS-RSTFINFlood"
    ]

    medium = [
        "DDoS-ICMP_Flood",
        "DDoS-PSHACK_Flood"
    ]

    if attack in high:
        threat = "HIGH"
    elif attack in medium:
        threat = "MEDIUM"
    else:
        threat = "LOW"

    return {
        "prediction": attack,
        "confidence": round(confidence, 2),
        "threat_level": threat
    }