from fastapi import APIRouter

from backend.models import DeviceData
from backend.predict_models import ThreatFeatures

from backend.database import (
    insert_device_data,
    insert_prediction,
    get_latest_device_data
)

from backend.ml_service import predict_attack
from backend.llm_service import generate_security_analysis

from rag.rag_service import retrieve_information

router = APIRouter()


@router.post("/device-data")
def receive_device_data(data: DeviceData):

    insert_device_data(data)

    return {
        "message": "Data stored successfully",
        "received_data": data
    }


@router.post("/predict-threat")
def predict_threat(data: ThreatFeatures):

    # Demo telemetry (later this will come from ESP32)
    telemetry = get_latest_device_data()
    if telemetry is None:
        telemetry = {
        "temperature": 0,
        "cpu_usage": 0,
        "packet_rate": 0,
        "failed_login": 0,
        "wifi_signal": 0
    }

    # ML Prediction
    result = predict_attack(
        data.model_dump(by_alias=True)
    )

    # Save prediction into database
    insert_prediction(
        result["prediction"],
        result["confidence"],
        result["threat_level"]
    )

    # Retrieve cybersecurity knowledge (RAG)
    rag_information = retrieve_information(
        result["prediction"]
    )

    # Generate AI explanation using RAG
    ai_analysis = generate_security_analysis(
        result["prediction"],
        result["confidence"],
        telemetry,
        rag_information
    )

    # Return everything
    return {
        "prediction": result["prediction"],
        "confidence": result["confidence"],
        "threat_level": result["threat_level"],
        "rag_information": rag_information,
        "ai_analysis": ai_analysis
    }