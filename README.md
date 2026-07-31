# 🛡️ AI-Powered IoT Cybersecurity Threat Detection System

A real-time IoT cybersecurity pipeline that combines a trained machine-learning classifier, MQTT telemetry ingestion, Retrieval-Augmented Generation (RAG), and Google Gemini analysis to detect attacks, explain risk, and visualize results through a Streamlit dashboard.

---

## 📌 Project Overview

This repository processes telemetry from an ESP32-style IoT device and maps it into the feature format expected by the threat-detection model. The backend receives the transformed features, performs a prediction, retrieves relevant mitigation context from the local knowledge base, and generates a security explanation using Gemini.

The workflow is:

- Device telemetry is published through MQTT
- A subscriber in the backend ingests the payload
- Telemetry is stored in SQLite and converted into ML-ready features
- A Random Forest classifier predicts the attack class
- RAG retrieves the threat-specific knowledge snippet
- Gemini generates an AI security report
- The Streamlit dashboard renders live telemetry and threat history

---

## 📸 Dashboard Screenshots

<p align="center">
  <img src="images/Screenshot 2026-07-31 114559.png" alt="Telemetry and threat monitoring screenshot" width="48%" />
    <img src="images\Screenshot 2026-07-31 114658.png" alt="AI IoT dashboard screenshot" width="48%" />
</p>

These visuals show the live telemetry and threat monitoring experience delivered by the Streamlit dashboard.

---

## 🏗️ System Architecture

```text
ESP32 / IoT Device
    │
    │ MQTT Publish
    ▼
Mosquitto Broker
    │
    ▼
backend/mqtt.py
    │
    ├─> Store telemetry in SQLite
    ├─> Map telemetry to ML features
    └─> POST prediction request to FastAPI

FastAPI Backend (backend/main.py)
    │
    ├─> /device-data
    └─> /predict-threat

Machine Learning Inference
    │
    ├─> Random Forest model
    ├─> Threat confidence + severity
    └─> Prediction persistence in SQLite

RAG + LLM Layer
    │
    ├─> knowledge_base.txt / rag_service.py
    └─> Gemini security reasoning via llm_service.py

Streamlit Dashboard
    │
    └─> Live telemetry, threat stats, and recent predictions
```

---

## 🚀 Features

- Real-time IoT telemetry ingestion over MQTT
- FastAPI backend for prediction and data ingestion
- Random Forest-based attack classification
- Threat severity labeling: HIGH / MEDIUM / LOW
- RAG-powered knowledge retrieval for relevant threat context
- Gemini-based security analysis generation
- SQLite persistence for device telemetry and predictions
- Streamlit dashboard for monitoring and visualization
- End-to-end sample workflow using local test payloads

---

## 🧠 Model and Data

### ML model

- Random Forest classifier
- Feature mapping pipeline built from MQTT telemetry
- Confidence score returned as a percentage

### Data source

- The project is designed around the CICIoT2023-style telemetry dataset format
- Sample data and project-specific feature data are available under the `datasets/` folder

### Expected outputs

- Trained model artifacts in `models/`
- Results and explainability outputs in `results/`

---

## 📂 Repository Structure

```text
AI-Powered-IoT-Cybersecurity-Threat-Detection-System/
├── backend/
│   ├── __init__.py
│   ├── database.py
│   ├── feature_mapper.py
│   ├── llm_service.py
│   ├── main.py
│   ├── ml_service.py
│   ├── models.py
│   ├── mqtt.py
│   ├── predict_models.py
│   ├── routes.py
│   └── README.md
├── dashboard/
│   ├── app.py
│   ├── dashboard_data.py
│   └── README.md
├── docs/
├── knowledge_base/
│   ├── ddos.md
│   ├── firewall.md
│   ├── icmp_flood.md
│   ├── ids.md
│   ├── mitigation.md
│   ├── nist.md
│   ├── tcp_flood.md
│   └── udp_flood.md
├── ml/
│   ├── datasets_loader.py
│   ├── explain.py
│   ├── explore.py
│   ├── predict.py
│   ├── preprocess.py
│   ├── README.md
│   ├── tempCodeRunnerFile.py
│   └── train.py
├── models/
│   └── README.md
├── rag/
│   ├── build_index.py
│   ├── knowledge_base.txt
│   ├── rag_service.py
│   └── README.md
├── results/
├── src/
│   └── main.cpp
├── tests/
│   ├── test_gemini.py
│   ├── test_mapper.py
│   ├── test_model.py
│   ├── test_mqtt_publish.py
│   ├── test_payload.json
│   ├── test_predict.py
│   └── test_rag.py
├── datasets/
│   └── iot_dataset.csv
├── platformio.ini
├── requirements.txt
├── reset_predictions_table.py
├── README.md
└── .env.example (if present in your environment)
```

---

## ⚙️ Tech Stack

### Backend

- FastAPI
- Uvicorn
- Pydantic

### MQTT + IoT

- Mosquitto Broker
- Paho-MQTT
- ESP32 firmware via PlatformIO

### Machine Learning

- Scikit-Learn
- Pandas
- NumPy
- Joblib
- SHAP

### AI and RAG

- Google Gemini API
- Retrieval-Augmented Generation with local knowledge artifacts
- Sentence Transformers / Transformers stack

### Dashboard

- Streamlit
- Streamlit AutoRefresh

### Database

- SQLite

---

## 📦 Installation

### 1) Clone the repository

```bash
git clone <your-repo-url>
cd AI-Powered-IoT-Cybersecurity-Threat-Detection-System-main
```

### 2) Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) Configure Gemini API key

Create a `.env` file in the project root and add:

```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```

The backend loads this key through `backend/llm_service.py`.

---

## ▶️ Running the Project

### Start the FastAPI backend

```bash
python -m uvicorn backend.main:app --reload --port 8000
```

API docs should be available at:

```text
http://127.0.0.1:8000/docs
```

### Start the MQTT subscriber

Make sure a Mosquitto broker is running locally on `localhost:1883`.

Then launch the subscriber:

```bash
python -m backend.mqtt
```

This module subscribes to the `iot/device01/telemetry` topic, converts incoming telemetry to model features, and sends predictions to the backend.

### Launch the Streamlit dashboard

```bash
python -m streamlit run dashboard/app.py
```

### Publish a sample telemetry payload

```bash
mosquitto_pub -h localhost -t iot/device01/telemetry -f tests/test_payload.json
```

---

## 🏋️ Model Training and Analysis

### Train the model

```bash
python ml/train.py
```

### Run explainability analysis

```bash
python ml/explain.py
```

This can generate SHAP-related outputs and feature-importance artifacts.

---

## 🧪 Testing

You can verify the major components with the repository test suite:

```bash
python tests/test_predict.py
python tests/test_mapper.py
python tests/test_rag.py
python tests/test_mqtt_publish.py
```

---

## 📚 Backend API

### `POST /device-data`

Stores inbound device telemetry into the SQLite `device_data` table.

### `POST /predict-threat`

Takes ML-ready input features and returns:

```json
{
  "prediction": "DDoS-TCP_Flood",
  "confidence": 99.98,
  "threat_level": "HIGH",
  "rag_information": "...",
  "ai_analysis": "..."
}
```

---

## 🔐 Threat Severity Mapping

| Confidence Range | Threat Level |
|------------------|--------------|
| > 90%            | HIGH         |
| 60% - 90%        | MEDIUM       |
| < 60%            | LOW          |

---

## 📸 Result Artifacts

The project writes model evaluation and interpretation artifacts into the `results/` directory and also creates the SQLite database file `iot_security.db` during runtime.

---

## 📌 Notes

- The dashboard depends on the backend being available and on `iot_security.db` being populated by the MQTT pipeline.
- If Gemini calls fail, the backend still returns the prediction result and stores a fallback error message in the database.
- For local development, ensure the Mosquitto broker is running before starting the MQTT subscriber.

---

## 👨‍💻 Contributors

1. Mahi Ahalawat - 2501270021
2. Aishni Rathore - 2501270009
3. Govind Agarwal - 2501270026
4. Yashika Naryani - 2501270027
5. Kshitiz Goyal - 250170042

---

## 📄 License

This project is developed for educational and research purposes.


