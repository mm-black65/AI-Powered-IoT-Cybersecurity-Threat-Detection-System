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

    telemetry = get_latest_device_data()

    if telemetry is None:
        telemetry = {
            "temperature": 0,
            "cpu_usage": 0,
            "packet_rate": 0,
            "failed_login": 0,
            "wifi_signal": 0
        }

    result = predict_attack(data.model_dump(by_alias=True))

    try:
        rag_information = retrieve_information(result["prediction"])
    except Exception as e:
        rag_information = f"RAG Error: {e}"

    try:
        ai_analysis = generate_security_analysis(
            result["prediction"],
            result["confidence"],
            telemetry,
            rag_information
        )
    except Exception as e:
        ai_analysis = f"Gemini Error: {e}"

    insert_prediction(
        prediction=result["prediction"],
        confidence=result["confidence"],
        threat_level=result["threat_level"],
        rag_information=rag_information,
        ai_analysis=ai_analysis
    )

    return {
        "prediction": result["prediction"],
        "confidence": result["confidence"],
        "threat_level": result["threat_level"],
        "rag_information": rag_information,
        "ai_analysis": ai_analysis
    }