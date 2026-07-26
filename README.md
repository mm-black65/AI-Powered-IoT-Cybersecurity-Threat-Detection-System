# 🛡️ AI-Powered IoT Cybersecurity Threat Detection System

An intelligent cybersecurity platform that leverages machine learning, retrieval-augmented generation (RAG), and large language models (LLM) to detect and analyze network threats in real-time from IoT devices.

## 🎯 Features

- **Machine Learning Threat Detection**: Random Forest classifier to identify 8 different DDoS attack types
- **Real-Time Processing**: MQTT-based telemetry ingestion from ESP32 IoT devices
- **AI-Powered Analysis**: Google Gemini integration for intelligent threat explanations
- **Knowledge Base**: RAG system with cybersecurity threat documentation
- **Interactive Dashboard**: Streamlit-based UI for threat monitoring and analytics
- **SQLite Database**: Persistent storage for predictions and device telemetry
- **Confidence Scoring**: ML model provides confidence percentages for predictions
- **Threat Levels**: Automatic threat severity classification (HIGH/MEDIUM/LOW)

## 📊 Project Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   ESP32     │────────▶│  MQTT Broker │────────▶│  Backend    │
│  IoT Device │         │(Mosquitto)   │         │  (FastAPI)  │
└─────────────┘         └──────────────┘         └─────────────┘
                                                        │
                                    ┌───────────────────┼───────────────────┐
                                    │                   │                   │
                            ┌───────▼──────┐   ┌───────▼──────┐   ┌───────▼──────┐
                            │       ML      │   │     RAG      │   │     LLM      │
                            │   (Random     │   │  (Knowledge  │   │   (Gemini)   │
                            │   Forest)     │   │   Base)      │   │              │
                            └───────┬──────┘   └──────────────┘   └──────────────┘
                                    │
                            ┌───────▼──────────┐
                            │   SQLite DB      │
                            │  (Predictions &  │
                            │   Telemetry)     │
                            └──────────────────┘
                                    │
                            ┌───────▼──────────┐
                            │  Streamlit       │
                            │  Dashboard       │
                            └──────────────────┘
```

## 🏗️ Project Structure

```
├── backend/                    # FastAPI REST API & Core Services
│   ├── main.py                # FastAPI app entry point
│   ├── routes.py              # API endpoints
│   ├── models.py              # Pydantic models
│   ├── ml_service.py          # ML prediction engine
│   ├── llm_service.py         # Gemini LLM integration
│   ├── database.py            # SQLite operations
│   ├── mqtt.py                # MQTT listener
│   ├── feature_mapper.py       # Telemetry-to-ML conversion
│   ├── predict_models.py       # Threat feature model
│   └── README.md
│
├── ml/                         # Machine Learning Pipeline
│   ├── train.py               # Model training (Random Forest)
│   ├── predict.py             # Standalone prediction
│   ├── explore.py             # Dataset exploration
│   ├── preprocess.py          # Data preprocessing (placeholder)
│   ├── explain.py             # Model explainability (placeholder)
│   ├── datasets_loader.py      # Dataset utilities (placeholder)
│   ├── model.pkl              # Trained model artifact
│   ├── label_encoder.pkl      # Label encoder
│   └── README.md
│
├── rag/                        # Retrieval-Augmented Generation
│   ├── rag_service.py         # Knowledge base retrieval
│   ├── retrieve.py            # Advanced retrieval (placeholder)
│   ├── build_index.py         # Indexing engine (placeholder)
│   ├── knowledge_base.txt      # Cybersecurity documentation
│   └── README.md
│
├── dashboard/                  # Web UI & Visualization
│   ├── app.py                 # Streamlit dashboard
│   └── README.md
│
├── esp32/                      # IoT Device Firmware
│   ├── main.cpp               # Arduino/ESP32 firmware
│   └── README.md
│
├── models/                     # Model Artifacts
│   ├── random_forest.pkl
│   ├── label_encoder.pkl
│   ├── feature_names.pkl
│   └── README.md
│
├── datasets/                   # Data Assets
│   └── raw/
│       └── iot_dataset.csv    # Training dataset (43 features)
│
├── tests/                      # Test Suite
│   ├── test_predict.py        # ML prediction tests
│   ├── test_rag.py            # RAG retrieval tests
│   ├── test_mapper.py         # Feature mapping tests
│   ├── test_mqtt_publish.py   # MQTT tests
│   └── test_gemini.py         # LLM integration tests
│
├── docs/                       # Documentation
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Mosquitto MQTT broker
- Google Gemini API key
- ESP32 microcontroller (optional, for live device data)

### 1. Installation

```bash
# Clone repository
git clone <repo-url>
cd AI-Powered-IoT-Cybersecurity-Threat-Detection-System-main

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_api_key_here
```

### 3. Setup MQTT Broker (Optional for ESP32)

```bash
# Install Mosquitto
# Ubuntu/Debian: sudo apt-get install mosquitto mosquitto-clients
# macOS: brew install mosquitto
# Windows: Download from mosquitto.org

# Start broker
mosquitto
# Or: mosquitto -c /etc/mosquitto/mosquitto.conf
```

### 4. Train ML Model (if needed)

```bash
cd ml
python train.py
# This generates: ../models/random_forest.pkl, label_encoder.pkl, feature_names.pkl
```

### 5. Run Backend API

```bash
cd backend
uvicorn main:app --reload --port 8000
# API available at: http://127.0.0.1:8000/docs (Swagger UI)
```

### 6. Start Dashboard

```bash
cd dashboard
streamlit run app.py
# Dashboard available at: http://localhost:8501
```

### 7. (Optional) Start MQTT Listener

```bash
cd backend
python mqtt.py
# Listens for ESP32 telemetry on iot/device01/telemetry
```

## 📡 API Endpoints

### `POST /device-data`
Receive IoT device telemetry.
```json
{
  "device_id": "ESP32_001",
  "temperature": 28.5,
  "cpu_usage": 45.2,
  "packet_rate": 150,
  "failed_login": 2,
  "wifi_signal": -58
}
```

### `POST /predict-threat`
Predict threats from network features.
```json
{
  "flow_duration": 0,
  "Header_Length": 54,
  "Protocol Type": 6,
  ...
  "Weight": 141.55
}
```

**Response:**
```json
{
  "prediction": "DDoS-TCP_Flood",
  "confidence": 99.96,
  "threat_level": "HIGH",
  "rag_information": "...",
  "ai_analysis": "..."
}
```

## 🤖 Detected Threats

| Attack Type | Severity | Description |
|-------------|----------|-------------|
| DDoS-TCP_Flood | HIGH | Overwhelming TCP packets |
| DDoS-UDP_Flood | HIGH | Massive UDP packet flooding |
| DDoS-SYN_Flood | HIGH | SYN packet flood attack |
| DDoS-RSTFINFlood | HIGH | RST/FIN packet termination |
| DDoS-ICMP_Flood | MEDIUM | ICMP echo request flood |
| DDoS-PSHACK_Flood | MEDIUM | PSH/ACK packet flood |
| Benign | LOW | Normal traffic |

## 🧠 Machine Learning Model

- **Algorithm**: Random Forest Classifier (150 estimators)
- **Features**: 43 network traffic metrics
- **Classes**: 8 (7 attack types + benign)
- **Training**: 80/20 train-test split
- **Framework**: scikit-learn

### Key Features:
- Flow duration, packet rates, protocol types
- TCP/UDP flags (SYN, ACK, FIN, RST, etc.)
- Packet statistics (min, max, average, std)
- IP and LLC protocol detection

## 🔍 RAG System

Knowledge base includes:
- Attack descriptions and severity levels
- Recommended mitigation strategies
- Cybersecurity context for IoT threat response

## 💬 LLM Integration

The backend uses Google Gemini to generate human-readable security analysis for detected threats. The LLM output explains the attack, severity, and recommended actions.

## 🧪 Testing

Run project tests from the repository root:
```bash
pytest -q
```

## 📦 Requirements

Install dependencies with:
```bash
pip install -r requirements.txt
```

## 🛠️ Notes

- The project integrates ESP32 telemetry, MQTT ingestion, ML threat classification, RAG retrieval, and LLM analysis.
- Core components are implemented and available for end-to-end operation with proper configuration.

## 💬 LLM Integration

Google Gemini generates professional security analysis including:
1. What attack is happening
2. Why it's dangerous
3. Severity assessment
4. Recommended mitigation steps
5. Action urgency for administrators

## 📊 Dashboard Features

- **Real-time threat statistics** (HIGH/MEDIUM/LOW counts)
- **Device telemetry display** (temperature, CPU, WiFi signal)
- **Latest threat detection** (prediction, confidence, level)
- **AI Security Report generation**
- **Historical threat visualization**
- **Backend connectivity status**
- **Auto-refresh** (5-second intervals)

## 🧪 Testing

Run individual tests:
```bash
python tests/test_predict.py
python tests/test_rag.py
python tests/test_mapper.py
python tests/test_mqtt_publish.py
python tests/test_gemini.py
```

## ⚙️ Configuration Files

### Backend Configuration
- MQTT Broker: `localhost:1883`
- FastAPI Port: `8000`
- Database: `iot_security.db` (SQLite)

### ESP32 Configuration (in main.cpp)
- WiFi credentials required
- MQTT broker IP: `192.168.1.100` (update with your PC IP)
- Telemetry topic: `iot/device01/telemetry`

## 🔧 Troubleshooting

### Backend Won't Start
- Ensure port 8000 is not in use: `netstat -ano | findstr :8000`
- Check virtual environment is activated
- Verify dependencies are installed

### MQTT Connection Failed
- Start Mosquitto: `mosquitto`
- Check MQTT broker IP in `src/main.cpp`
- Ensure ESP32 can reach the broker

### Dashboard Not Loading
- Check Streamlit is installed: `pip install streamlit`
- Backend must be running
- Clear Streamlit cache: `streamlit cache clear`

### ML Model Errors
- Verify model files exist in `models/`
- Check feature order matches `feature_names.pkl`
- Retrain if model is corrupted: `python ml/train.py`

## 📝 What's Left (To-Do)

### Critical
- [ ] Fix `requirements.txt` encoding
- [ ] Complete `dashboard/app.py` implementation
- [ ] Complete `esp32/main.cpp` loop function
- [ ] Fix `test_gemini.py` missing parameter
- [ ] Add `.env` configuration file

### Important
- [ ] Setup MQTT broker
- [ ] Enhance feature mapping for real telemetry
- [ ] Add integration tests
- [ ] Complete subdirectory READMEs

### Optional
- [ ] Implement data preprocessing utilities
- [ ] Add model explainability (SHAP/LIME)
- [ ] Implement semantic search with embeddings
- [ ] Docker containerization
- [ ] Comprehensive logging system

## 📚 Documentation

- [Backend README](backend/README.md) - API & Services
- [ML README](ml/README.md) - Model Training & Evaluation
- [RAG README](rag/README.md) - Knowledge Base System
- [ESP32 README](esp32/README.md) - Device Firmware
- [Dashboard README](dashboard/README.md) - UI Components

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature/your-feature`
5. Create Pull Request

## 📄 License

MIT License

## 👥 Authors

1. Mahi Ahalawat - 2501270021
2. Aishni Rathore - 2501270009
3. Govind Agarwal - 2501270026
4. Yashika Naryani - 2501270027
5. Kshitiz Goyal - 250170042

---
